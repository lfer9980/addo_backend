import os


from app.usuarios.crud import UserCRUD
from app.usuarios.schemas import CreateUserSchema
from core.db.session import SessionFactory


async def create_admin_user() -> None:

    db = SessionFactory()

    username: str = os.getenv("ADMIN_USERNAME")
    password: str = os.getenv("ADMIN_PASSWORD")
    nombres: str = os.getenv("ADMIN_NOMBRES")
    apellidos: str = os.getenv("ADMIN_APELLIDOS")
    tipo_usuario: str = "admin"
    posicion: str = "Gerencia"
    avatar: str = ""

    user = await UserCRUD().get_by_username(
        username=username,
        db=db
    )

    if user is None:
        new_user = CreateUserSchema(
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password,
            confirm_password=password,
            tipo_usuario=tipo_usuario,
            posicion=posicion,
            avatar=avatar
        )
        await UserCRUD().create(user=new_user,
                                db=db)

        print("USER ADMIN CREATED!!")


async def create_default_user() -> None:

    db = SessionFactory()

    username: str = "default"
    password: str = "12345"
    nombres: str = "default"
    apellidos: str = "default"
    tipo_usuario: str = "colaborador"
    posicion: str = "auxiliar"
    avatar: str = ""

    user = await UserCRUD().get_by_username(
        username=username,
        db=db
    )

    if user is None:
        new_user = CreateUserSchema(
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password,
            confirm_password=password,
            tipo_usuario=tipo_usuario,
            posicion=posicion,
            avatar=avatar
        )
        await UserCRUD().create(user=new_user,
                                db=db)

        print("USER DEFAULT CREATED!!")