from fastapi_easystart.utils.enums.crud import CreateResponseCodeEnum, UpdateResponseCodeEnum, DeleteResponseCodeEnum
from fastapi_easystart.utils.enums.exceptions import ExceptionTypeEnum
from fastapi_easystart.utils.enums.response import ResponseKeyEnum


class ResponseEnum:
    RESPONSE_KEY = ResponseKeyEnum
    EXCEPTION = ExceptionTypeEnum
    CREATE = CreateResponseCodeEnum
    UPDATE = UpdateResponseCodeEnum
    DELETE = DeleteResponseCodeEnum
