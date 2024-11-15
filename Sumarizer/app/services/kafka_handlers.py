"""
Kafka event handling implementation for the summarizer service.

This module contains handlers for processing Kafka messages and
managing the lifecycle of summary requests through the system.

Typical usage:
    handler = KafkaEventHandler()
    await handler.start_listening()
"""

from typing import Dict, Any, Optional
from app.core.kafka import KafkaClient
from app.services.summarizer import SummarizerService
from app.models.summarizer import SummaryRequest
import asyncio
import logging
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)


class KafkaEventHandler:
    """
    Handler for processing Kafka events related to summarization.

    This class manages the lifecycle of summary requests from receipt
    through processing and notification of completion.

    Attributes:
        kafka (KafkaClient): Kafka client for message handling
        summarizer (SummarizerService): Service for text summarization
    """

    def __init__(self) -> None:
        """Initialize Kafka handler with required services."""
        self.kafka = KafkaClient()
        self.summarizer = SummarizerService()
        logger.info("Kafka event handler initialized")

    async def start_listening(self) -> None:
        """
        Start listening for summary requests from Kafka.

        This method runs indefinitely, processing incoming messages
        and handling any errors that occur during processing.

        Raises:
            Exception: If there's an unrecoverable error in the consumer
        """
        logger.info("Starting to listen for summary requests")
        try:
            async for message in self.kafka.consumer:
                try:
                    await self.handle_summary_request(message.value)
                    # Commit offset only after successful processing
                    self.kafka.consumer.commit()
                except Exception as e:
                    logger.error(
                        f"Error processing message {message.value}: {str(e)}\n"
                        f"Traceback: {traceback.format_exc()}"
                    )
        except Exception as e:
            logger.critical(f"Kafka consumer failed: {str(e)}")
            raise

    async def handle_summary_request(self, data: Dict[str, Any]) -> None:
        """
        Process an incoming summary request.

        Args:
            data: Dictionary containing request details including:
                - content: Text to summarize
                - user_id: ID of requesting user
                - request_id: Unique request identifier

        Raises:
            ValueError: If required data is missing
            Exception: If summarization fails
        """
        request_id = data.get("request_id")
        user_id = data.get("user_id")

        if not all([request_id, user_id, data.get("content")]):
            raise ValueError("Missing required request data")

        logger.info(f"Processing summary request {request_id} for user {user_id}")

        try:
            # Create summary request
            summary_request = SummaryRequest(
                content=data["content"],
                max_length=data.get("max_length"),
                min_length=data.get("min_length"),
            )

            # Process summary
            summary_result = await self.summarizer.summarize(summary_request)

            # Send completion notification
            await self.kafka.send_summary_completed(
                user_id=user_id,
                summary_data={
                    "request_id": request_id,
                    "summary": summary_result.summary,
                    "processing_time": summary_result.processing_time,
                    "chunks_processed": summary_result.chunks_processed,
                    "completed_at": datetime.utcnow().isoformat(),
                },
            )

            logger.info(f"Summary request {request_id} completed successfully")

        except Exception as e:
            logger.error(
                f"Failed to process summary request {request_id}: {str(e)}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            # Here you might want to send a failure notification
            # or implement retry logic
            raise
