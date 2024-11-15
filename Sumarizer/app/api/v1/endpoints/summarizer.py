from fastapi import APIRouter, HTTPException
from app.models.summarizer import SummaryRequest, SummaryResponse
from app.services.summarizer import SummarizerService

router = APIRouter()
summarizer_service = SummarizerService()

@router.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    """Generate summary for provided text content."""
    try:
        return await summarizer_service.summarize(request)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Summarization failed: {str(e)}"
        )
