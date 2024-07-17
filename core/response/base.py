from pydantic import BaseModel
from typing import Any, Dict, List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ResponseStructure(BaseModel):
    status_code: int = 200
    errors: Dict[str, str] = {}
    messages: List[str] = ['']
    data: Any


class CustomResponse(JSONResponse):
    def __init__(self, content: Any, status_code: int = 200, errors: Dict[str, str] = {},
                 messages: List[str] = [''],
                 *args, **kwargs) -> None:
        content = ResponseStructure(status_code=status_code, errors=errors, data=jsonable_encoder(content),
                                    messages=messages).dict()
        super().__init__(content, status_code, *args, **kwargs)
