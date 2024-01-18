# sender.py
from fastapi import HTTPException, status, BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_SMTP_USER,
    MAIL_PASSWORD=settings.EMAIL_SMTP_PASSWORD,
    MAIL_FROM=settings.EMAILS_FROM_EMAIL,
    MAIL_PORT=settings.EMAIL_SMTP_PORT,
    MAIL_SERVER=settings.EMAIL_SMTP_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


def send_email(to_email: EmailStr, subject: str, content: str, background_tasks: BackgroundTasks):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=content,
        subtype="html",
    )
    background_tasks.add_task(send_email_background, message)


async def send_email_background(message: MessageSchema):
    try:
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e))
