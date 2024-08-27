from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File
from fastapi_mail import FastMail, MessageSchema, MessageType

from core.mail.schemas import EmailSchema
from core.utils.token import Manager
from core.mail.config import CONFIG as MAIL_CONFIG

mail_router = APIRouter()


@mail_router.post('/send')
async def send_mail(background_tasks: BackgroundTasks,
                    email_data: EmailSchema = Depends(),
                    file: UploadFile = File(None),
                    current_session: Depends = Depends(Manager)):
    
    attachment_list = []
    
    if file: 
        attachment_list.append(file)
        

    message = MessageSchema(
        recipients = [email_data.email],
        subject = email_data.subject,
        body = email_data.body,
        token = email_data.subject,
        attachments = attachment_list,
        subtype="html"
    )

    fm = FastMail(MAIL_CONFIG)

    await fm.send_message(message)

    return {'message': 'Message sent!'}
