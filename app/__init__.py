import dotenv
from fastapi import FastAPI, Request
from starlette.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from api import router

from core import (VERSION,
                  OPEN_API_TITLE,
                  OPEN_API_DESCRIPTION,
                  API_PREFIX)

from core.config import config
from core.response import CustomResponse
from app.usuarios.default_user import create_admin_user, create_default_user


def init_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI) -> None:
    app.include_router(router,
                       prefix=API_PREFIX)


def init_listeners(app: FastAPI) -> None:
    async def http_exception_handler(request, exc: HTTPException):
        response = {
            'status_code': exc.status_code,
            'errors': {f'{exc.status_code}': exc.detail},
            'content': {},
        }

        return CustomResponse(**response)

    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        inputs = [input_data['loc'][-1] for input_data in exc.errors()]
        messages = [error['msg'] for error in exc.errors()]

        response = {
            'status_code': 422,
            'errors': dict(zip(inputs, messages)),
            'content': {}
        }

        return CustomResponse(**response)

    async def response_exception_handler(request: Request, exc: HTTPException):
        response = {
            'status_code': 422,
            'errors': {f'{exc.status_code}': exc.detail},
            'content': {}
        }

        return CustomResponse(**response)

    # app.add_exception_handler(HTTPException,
    #                           http_exception_handler)  # noqa
    #
    # app.add_exception_handler(RequestValidationError,
    #                           request_validation_exception_handler)  # noqa
    #
    # app.add_exception_handler(ValueError,
    #                           response_exception_handler) # noqa


def init_super_user(app: FastAPI) -> None:

    @app.on_event('startup') # noqa
    async def startup() -> None:
        await create_admin_user()
        await create_default_user()


def create_app() -> FastAPI:
    dotenv.load_dotenv()
    app = FastAPI(
        version=VERSION,
        title=OPEN_API_TITLE,
        description=OPEN_API_DESCRIPTION,
        swager_url="/",
        docs_url=None if config.ENV == "production" else "/",
        redoc_url=None if config.ENV == "production" else "/redoc",
        openapi_url=None if config.ENV == "production" else "/openapi.json",
        default_response_class=CustomResponse,
        debug=False if config.ENV == "production" else True,
    )

    init_cors(app=app)
    init_routers(app=app)
    init_listeners(app=app)
    init_super_user(app=app)

    return app


app = create_app()
