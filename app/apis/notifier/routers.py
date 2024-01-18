from fastapi import APIRouter, BackgroundTasks
from pydantic import EmailStr
from app.core.email.sender import send_email


router = APIRouter()


@router.post("/send-email")
async def send_test_mail(email: EmailStr, background_tasks: BackgroundTasks):
    subject = "CloudStorage: Test Email"
    content = "<h1>Hello, this is a test email!</h1>"
    send_email(to_email=email, subject=subject, content=content,
               background_tasks=background_tasks)
    return {"message": "Email sent successfully!"}
