from dotenv import load_dotenv
import os

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),  # Ganti dengan email Anda
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),  # Gunakan password akun atau App Password
    MAIL_FROM=os.getenv('MAIL_FROM'),     # Sama dengan MAIL_USERNAME
    MAIL_PORT=587,                        # Port SMTP Gmail
    MAIL_SERVER="smtp.gmail.com",         # Server SMTP Gmail
    MAIL_FROM_NAME="Auxesia",             # Nama pengirim
    MAIL_STARTTLS=True,                   # Harus True untuk Gmail
    MAIL_SSL_TLS=False,                   # Jangan gunakan SSL/TLS
    USE_CREDENTIALS=True,                 # Autentikasi diperlukan
    VALIDATE_CERTS=True                   # Validasi sertifikat
)


FM = FastMail(conf)

async def VerifyEmail(email : EmailStr, token : str) :
    html = f"""<p>Hi, this is a test mail. Thanks for using FastAPI-Mail. Verify your email:</p><br>
            <a href="127.0.0.1:8000/auth/verifyemail?token={token}" 
            style="display: inline-block; background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; text-decoration: none; cursor: pointer;">
            Verify
            </a>"""


    message = MessageSchema(
        subject="Auxesia Email Verification",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    print(f"127.0.0.1:8000/auth/verifyemail?token={token}")
    await FM.send_message(message)
    return "Verification mail has been sent"