from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from core.utils.token import Manager
from app.usuarios.crud import UserCRUD
from core.db.session import SessionFactory


@Manager.user_loader()
async def load_user(username: str):

    db: Session = SessionFactory()

    user = await UserCRUD().get_by_username(username=username, db=db)
    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

