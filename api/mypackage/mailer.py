from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from decouple import config
from typing import List

#This will be used if there is a need to send emails
#Since the project is currently deployed on Deta, 
#Sending emails is a headache, plus not really neccessary

conf = ConnectionConfig(
    MAIL_USERNAME = config("MAIL_USERNAME"),
    MAIL_PASSWORD = config("MAIL_PASSWORD"),
    MAIL_FROM = config("MAIL_FROM"),
    MAIL_PORT = 587,
    MAIL_SERVER = config("MAIL_SERVER"),
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
)

html = f"""
        <p>Thanks for using A random project</p> 
        """

async def simple_send(token: str, email:List):
    link: str = f"https://wby808.deta.dev/users/activate/{token}"

    message = MessageSchema(
        subject="Activate Your Random Project Account",
        recipients=email,  # List of recipients, as many as you can pass 
        body=html,
        subtype="html"
        )

    fm = FastMail(conf)
    await fm.send_message(message)
    return {"data":"Check your email for account activation link"}