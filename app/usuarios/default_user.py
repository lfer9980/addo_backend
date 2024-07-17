import os


from app.usuarios.crud import UserCRUD
from app.usuarios.schemas import CreateUserSchema
from core.db.session import SessionFactory


async def create_admin_user() -> None:

    db = SessionFactory()

    username: str = os.getenv("ADMIN_USERNAME")
    password: str = os.getenv("ADMIN_PASSWORD")
    user_type: str = "admin"
    posicion: str = "Gerencia"
    avatar: str = ""

    user = await UserCRUD().get_by_username(
        username=username,
        db=db
    )

    if user is None:
        new_user = CreateUserSchema(
            username=username,
            password=password,
            confirm_password=password,
            user_type=user_type,
            posicion=posicion,
            avatar=avatar
        )
        await UserCRUD().create(user=new_user,
                                db=db)

        print("USER ADMIN CREATED!!")
