from kafka import KafkaProducer, KafkaConsumer
import json
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AuthKafkaClient:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        self.consumer = KafkaConsumer(
            'user_events',
            bootstrap_servers=settings.KAFKA_SERVERS,
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
            group_id='auth_group'
        )
    
    async def send_user_event(self, event_type: str, user_data: dict):
        """Send user-related events to other services."""
        try:
            self.producer.send(
                'user_events',
                {
                    'event_type': event_type,
                    'user_data': user_data
                }
            )
            logger.info(f"User event {event_type} sent for user {user_data['id']}")
        except Exception as e:
            logger.error(f"Failed to send user event: {e}")