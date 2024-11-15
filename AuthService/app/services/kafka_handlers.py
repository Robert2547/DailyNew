from app.core.kafka import AuthKafkaClient
import logging
from app.services.auth import AuthService

logger = logging.getLogger(__name__)

class AuthEventHandler:
    def __init__(self):
        self.kafka = AuthKafkaClient()
        self.auth_service = AuthService()
        
    async def notify_user_created(self, user_data: dict):
        """Notify other services when a user is created."""
        await self.kafka.send_user_event('user_created', user_data)
        
    async def notify_user_logged_in(self, user_id: int):
        """Notify other services when a user logs in."""
        await self.kafka.send_user_event('user_logged_in', {'id': user_id})