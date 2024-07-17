from fastapi import APIRouter, Depends, BackgroundTasks, UploadFile, File
from fastapi_mail import FastMail, MessageSchema, MessageType

from core.mail.schemas import EmailSchema
from core.utils.token import Manager
from core.mail.config import CONFIG as MAIL_CONFIG

mail_router = APIRouter()


@mail_router.post('/send')
async def send_mail(content: EmailSchema = Depends(),
                    file: UploadFile = File(None),
                    current_session: Depends = Depends(Manager)):
    content = content.model_dump()

    message = MessageSchema(
        subject=content.get('asunto'),
        recipients=[content.get('email')],
        body=content.get('texto'),
        subtype=MessageType.plain,
        attachments=[file],
    )

    fm = FastMail(MAIL_CONFIG)

    await fm.send_message(message)

    return {'message': 'Message sent!'}
