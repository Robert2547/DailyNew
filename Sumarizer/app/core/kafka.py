# summarizer_service/app/core/kafka.py
"""
Kafka client implementation for the summarizer service.

This module provides Kafka integration for asynchronous message handling
in the summarizer service. It includes producers and consumers for
handling summary requests and notifications.

Typical usage:
    client = KafkaClient()
    await client.send_summary_completed(user_id=1, summary_data={...})
"""

from typing import Any, Dict, Optional
from kafka import KafkaProducer, KafkaConsumer
import json
from app.core.config import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class KafkaClient:
    """
    Kafka client for handling message production and consumption.

    This class manages Kafka connections and provides methods for sending
    and receiving messages related to the summarization service.

    Attributes:
        producer (KafkaProducer): Kafka producer instance
        consumer (KafkaConsumer): Kafka consumer instance for summary requests
    """

    def __init__(self) -> None:
        """Initialize Kafka producer and consumer connections."""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_SERVERS,
                value_serializer=self._serialize_message,
                acks="all",  # Wait for all replicas
                retries=3,  # Retry failed sends
                retry_backoff_ms=500,  # Backoff time between retries
            )

            self.consumer = KafkaConsumer(
                "summary_requests",
                bootstrap_servers=settings.KAFKA_SERVERS,
                value_deserializer=self._deserialize_message,
                group_id="summarizer_group",
                auto_offset_reset="earliest",
                enable_auto_commit=False,  # Manual commit for better control
                session_timeout_ms=30000,  # 30 seconds
                max_poll_interval_ms=300000,  # 5 minutes
            )

            logger.info("Kafka client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka client: {str(e)}")
            raise

    @staticmethod
    def _serialize_message(message: Dict[str, Any]) -> bytes:
        """
        Serialize message to JSON bytes.

        Args:
            message: Dictionary containing message data

        Returns:
            bytes: JSON-encoded message

        Raises:
            json.JSONEncodeError: If message serialization fails
        """
        try:
            return json.dumps(message).encode("utf-8")
        except json.JSONEncodeError as e:
            logger.error(f"Message serialization failed: {str(e)}")
            raise

    @staticmethod
    def _deserialize_message(message: bytes) -> Dict[str, Any]:
        """
        Deserialize message from JSON bytes.

        Args:
            message: JSON-encoded message bytes

        Returns:
            dict: Deserialized message data

        Raises:
            json.JSONDecodeError: If message deserialization fails
        """
        try:
            return json.loads(message.decode("utf-8"))
        except json.JSONDecodeError as e:
            logger.error(f"Message deserialization failed: {str(e)}")
            raise

    async def send_summary_completed(
        self, user_id: int, summary_data: Dict[str, Any]
    ) -> None:
        """
        Send completion notification for processed summary.

        Args:
            user_id: ID of the user who requested the summary
            summary_data: Dictionary containing summary results and metadata

        Raises:
            KafkaError: If message sending fails
        """
        message = {
            "user_id": user_id,
            "summary": summary_data,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "completed",
        }

        try:
            self.producer.send("summary_completed", message).get(
                timeout=10
            )  # Wait for send confirmation
            logger.info(f"Summary completion notification sent for user {user_id}")
        except Exception as e:
            logger.error(
                f"Failed to send summary completion for user {user_id}: {str(e)}"
            )
            raise
