"""Email utility functions."""

from typing import List, Optional
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmailUtils:
    """Email utility class for sending emails."""

    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USER,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.EMAILS_FROM_EMAIL,
            MAIL_PORT=settings.SMTP_PORT,
            MAIL_SERVER=settings.SMTP_HOST,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
        )
        self.fast_mail = FastMail(self.conf)

    async def send_email(
        self,
        email_to: str | List[str],
        subject: str,
        body: str,
        template_name: Optional[str] = None,
    ) -> bool:
        """
        Send email to specified recipients.

        Args:
            email_to: Recipient email address(es)
            subject: Email subject
            body: Email body
            template_name: Optional template name

        Returns:
            bool: True if email sent successfully
        """
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[email_to] if isinstance(email_to, str) else email_to,
                body=body,
                subtype="html",
            )
            await self.fast_mail.send_message(message)
            logger.info(f"Email sent successfully to {email_to}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
