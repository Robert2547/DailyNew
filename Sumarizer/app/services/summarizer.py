from transformers import AutoTokenizer, AutoModelForSeq2SeqLm
import asyncio
import time
from typing import List, Tuple
from app.core.config import settings
from app.models.summarizer import SummaryRequest, SummaryResponse
from app.core.cache import CacheManager


class SummarizerService:
    def __init__(self):
        self.tokenizer, self.model = self._load_model()
        self.cache = CacheManager()

    def _load_model(self) -> Tuple[AutoTokenizer, AutoModelForSeq2SeqLm]:
        """Load the tokenizer and model."""
        start = time.perf_counter()
        tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        model = AutoModelForSeq2SeqLm.from_pretrained(settings.MODEL_NAME)
        print(f"Model loaded in {time.perf_counter()-start:.2f} seconds")
        return tokenizer, model

    async def summarize(self, request: SummaryRequest) -> SummaryResponse:
        """Generate summary for given content."""
        # Check cache first
        cached_summary = await self.cache.get_summary(request.content)
        if cached_summary:
            return SummaryResponse(
                summary=cached_summary, processing_time=0, chunks_processed=0
            )

        start_time = time.perf_counter()
        chunk_queue = asyncio.Queue(maxsize=settings.MAX_QUEUE_SIZE)

        # Start producer/consumer tasks
        producer = asyncio.create_task(
            self._produce_chunks(chunk_queue, request.content)
        )
        consumer = asyncio.create_task(self._consume_chunks(chunk_queue, request))

        await producer
        summaries = await consumer

        # Combine summaries and cache result
        full_summary = " ".join(summaries)
        await self.cache.set_summary(request.content, full_summary)

        return SummaryResponse(
            summary=full_summary,
            processing_time=time.perf_counter() - start_time,
            chunks_processed=len(summaries),
        )

    async def _produce_chunks(self, queue: asyncio.Queue, content: str):
        """Split content into chunks and add to queue."""
        chunks = self._split_text(
            content, max_tokens=settings.MAX_CHUNK_SIZE, overlap=settings.CHUNK_OVERLAP
        )
        for chunk in chunks:
            await queue.put(chunk)
        await queue.put(None)  # Signal completion

    async def _consume_chunks(
        self, queue: asyncio.Queue, request: SummaryRequest
    ) -> List[str]:
        """Process chunks from queue into summaries."""
        summaries = []
        while True:
            chunk = await queue.get()
            if chunk is None:
                break
            summary = self._summarize_chunk(chunk, request)
            summaries.append(summary)
            queue.task_done()
        return summaries

    def _split_text(self, content: str, max_tokens: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks."""
        paragraphs = content.split("\n")
        chunks = []
        current_chunk = ""
        current_tokens = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            tokens = len(paragraph.split())

            if current_tokens + tokens <= max_tokens:
                current_chunk += f"{paragraph} "
                current_tokens += tokens
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                overlap_text = " ".join(current_chunk.split()[-overlap:])
                current_chunk = f"{overlap_text} {paragraph} "
                current_tokens = len(current_chunk.split())

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def _summarize_chunk(self, chunk: str, request: SummaryRequest) -> str:
        """Summarize a single chunk of text."""
        inputs = self.tokenizer(
            chunk,
            max_length=request.max_length or 1024,
            return_tensors="pt",
            truncation=True,
        )

        summary_ids = self.model.generate(
            **inputs,
            min_length=request.min_length or 50,
            max_length=request.max_length or 1024,
        )

        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
