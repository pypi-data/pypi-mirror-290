from fastapi import status

from fastapi_easystart.exception import BaseHTTPException
from fastapi_easystart.utils.enums import ResponseEnum


class InvalidInputException(BaseHTTPException):
    response_code = ResponseEnum.EXCEPTION.VALIDATION_ERROR.response_key
    message = ResponseEnum.EXCEPTION.VALIDATION_ERROR.value


class UnsupportedMediaTypeException(BaseHTTPException):
    message = ResponseEnum.EXCEPTION.UNSUPPORTED_MEDIA_TYPE.value
    response_code = ResponseEnum.EXCEPTION.UNSUPPORTED_MEDIA_TYPE.response_key
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
