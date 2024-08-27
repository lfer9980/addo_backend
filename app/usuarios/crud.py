from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session, Query

from core.db import BaseCRUD
from app.usuarios.schemas import *
from core.utils.hashing import Hasher
from app.models.usuarios import UsuarioModel


class UserCRUD(BaseCRUD):

    @staticmethod
    async def _has_admin(db: Session) -> bool:
        
        user = db.query(UsuarioModel).filter(
            UserTypeEnum.SupeAdmin == UsuarioModel.tipo_usuario
        ).first()

        if user is None:
            return False
        return True

    @classmethod
    async def create(cls, db: Session, user: CreateUserSchema) -> UserSchema:

        user_exists = await cls._filter_by(db=db,
                                           data=user.username,
                                           key='username',
                                           table=UsuarioModel)

        if user_exists.first():
            raise HTTPException(status_code=409,
                                detail="El nombre de usuario ya existe")

        if await cls._has_admin(db=db) and user.tipo_usuario == UserTypeEnum.SupeAdmin:
            raise HTTPException(status_code=409,
                                detail="El usuario administrador ya existe!")

        hashed_password = Hasher.get_password_hash(user.password)

        user_data = user.model_dump()
        user_data.pop('confirm_password', None)
        user_data['password'] = hashed_password

        db_user = UsuarioModel(**user_data)

        await cls._save(db=db,
                        data=db_user)

        return UserSchema.model_validate(db_user)

    @classmethod
    async def update_user(cls, db: Session, 
                          user_update_username: str,
                          user_updating_username: str,
                          user: UpdateUserSchema) -> UserSchema:

        old_user: Query = await cls._filter_by(db=db,
                                               table=UsuarioModel,
                                               key='username',
                                               data=user_update_username)
        
        old_user: UsuarioModel | None = old_user.first()

        user_updating: Query = await cls._filter_by(db=db,
                                                    table=UsuarioModel,
                                                    key='username',
                                                    data=user_updating_username)
        
        user_updating: UsuarioModel | None = user_updating.first()

        if old_user is None:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado!")

        if user_updating is None:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado!")

        if user_updating.tipo_usuario == UserTypeEnum.Supervisor:

            if user.tipo_usuario in [UserTypeEnum.Supervisor, UserTypeEnum.SupeAdmin]:
                raise HTTPException(status_code=403,
                                    detail="No estas autorizado para modificar este perfil!")

        new_user = user.model_dump()

        if user.new_password:
            hashed_password = Hasher.get_password_hash(user.new_password)
            new_user['password'] = hashed_password

        for key, value in new_user.items():
            if value is not None:
                setattr(old_user, key, value)

        await cls._update(db=db,
                          data=old_user)

        return UserSchema.model_validate(old_user)

    @classmethod
    async def update_me(cls, db: Session,
                        user_id: str, 
                        user: UpdateOwnUserSchema) -> UserSchema:

        old_user: Query = await cls._filter_by(db=db,
                                               table=UsuarioModel,
                                               key='id',
                                               data=user_id)
        
        old_user: None | UsuarioModel = old_user.first()

        if old_user is None:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado!")

        if not Hasher.verify_password(user.old_password, old_user.password):
            raise HTTPException(status_code=401,
                                detail="La contrasena es incorrecta")

        hashed_password = Hasher.get_password_hash(user.new_password)

        new_user = user.model_dump()
        new_user.pop('confirm_password', None)
        new_user['password'] = hashed_password

        for key, value in new_user.items():
            if value is not None:
                setattr(old_user, key, value)

        await cls._update(db=db,
                          data=old_user)

        return UserSchema.model_validate(old_user)

    @classmethod
    async def delete(cls, db: Session, username: str) -> None:

        user: Query = await cls._filter_by(db=db,
                                           table=UsuarioModel,
                                           key='username',
                                           data=username)
        
        user: UsuarioModel | None = user.first()
        
        if user is None:
            raise HTTPException(status_code=404,
                                detail="Usuario no encontrado")

        if user.tipo_usuario is UserTypeEnum.SupeAdmin:
            raise HTTPException(status_code=403,
                                detail="No puedes eliminar un usuario administrador")
        
        if user.username == "default":
            raise HTTPException(status_code=403,
                    detail="No puedes eliminar el usuario default") 

        await cls._delete(db=db,
                          data=user)

    @classmethod
    async def get_by_username(cls, db: Session, username: str):
        user: Query = await cls._filter_by(db=db, key='username', data=username, table=UsuarioModel)
        
        user: UsuarioModel | None = user.first()

        return user.to_dict() if user else None

    @classmethod
    async def get_one(cls, db: Session, username: str) -> UserSchema:

        user: Query = await cls._filter_by(db=db,
                                            table=UsuarioModel,
                                            key='username',
                                            data=username)
        user = user.first()

        if user is None:
            raise HTTPException(
                status_code=400,
                detail='usuario no encontrado'
            )

        return UserSchema.model_validate(user)

    @classmethod
    async def get_all(cls, db: Session,
                      page: int = 1, 
                      page_size: int = 10) -> List[UserSchema]:

        usuarios = await cls._get_all(db=db,
                                      page=page,
                                      page_size=page_size,
                                      table=UsuarioModel)
        
        usuarios_filter = filter(lambda x: x.username != "superuser" and x.username != "default", usuarios)
        usuarios_filter = list(usuarios_filter)

        return [UserSchema.model_validate(usuario) for usuario in usuarios_filter]