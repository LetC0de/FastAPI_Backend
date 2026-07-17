from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, BaseModel
from typing import List


conf = ConnectionConfig(
    MAIL_USERNAME = "abhishekjiiofficial86@gmail.com",
    MAIL_PASSWORD = "kxrf qtwj jkkh nfig",
    MAIL_FROM = "abhishekjiiofficial86@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Abhishek Nishad",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)



async def send_email(emails:List[str]):
    html = """<p>Thankyou for Registration</p> """

    message = MessageSchema(
        subject="Registration Conformation",
        recipients=[emails],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"message": "email has been sent"}