from pydantic import EmailStr

from core.schemas import BaseSchema


class EmailSchema(BaseSchema):
    email: EmailStr
    asunto: str
    texto: str
    token: str
