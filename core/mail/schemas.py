from pydantic import EmailStr

from core.schemas import BaseSchema
class EmailSchema(BaseSchema):
    email: EmailStr
    subject: str
    body:str
    token: str