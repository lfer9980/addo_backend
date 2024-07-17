import pytz
from datetime import datetime, timedelta
from fastapi import (APIRouter, Depends)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException

from core.utils.token import Manager
from app.auth.utils import load_user
from core.utils.hashing import Hasher
from core import ACCESS_TOKEN_EXPIRE_MINUTES


auth_router = APIRouter()


@auth_router.post('/login', response_class=JSONResponse)
async def login(request: OAuth2PasswordRequestForm = Depends()):

    username = request.username
    password = request.password

    user = await load_user(username)
    
    if user is None:
        raise InvalidCredentialsException

    if not Hasher.verify_password(plain_password=password,
                                  hashed_password=user['password']):
        raise InvalidCredentialsException

    """ for obtain the timezone """
    timezone = pytz.timezone('Etc/GMT+6')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    date_creation = datetime.now(timezone)
    expiration_time = date_creation + access_token_expires
    
    access_token = Manager.create_access_token(
        data=dict(sub=username),
        expires=access_token_expires
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        "expires_time": expiration_time.isoformat(),
        "date": date_creation.isoformat(),
        }
