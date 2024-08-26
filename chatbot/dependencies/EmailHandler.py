from typing import List

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
import os

from chatbot.logger import logger


class EmailSchema(BaseModel):
    email: List[EmailStr]
    subject: str
    body: str


class EmailHandler:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
        )
        self.fm = FastMail(self.conf)

    async def send_email(self, email: EmailSchema):
        message = MessageSchema(
            subject=email.subject,
            recipients=email.email,
            body=email.body,
            subtype="html"
        )
        await self.fm.send_message(message)

        logger.debug("Email sent successfully to %s", email.email)
