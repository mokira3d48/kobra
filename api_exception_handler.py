from typing import Any, Optional
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status


class CustomAPIException(APIException):
    
    def __init__(self, detail: Optional[Any]=None, code: Optional[str]=None) -> None:
        super().__init__(detail, code)
        self.detail = detail if detail is not None else self.__class__.default_detail
        self.code = code if code is not None else self.__class__.default_code


class APIExceptionSerializer(serializers.Serializer):
    detail = serializers.JSONField(read_only=True)
    code = serializers.CharField(read_only=True)


class ValidationError(CustomAPIException):
    status_code = status.HTTP_400_BAD_REQUEST


class NotFound(CustomAPIException):
    status_code = status.HTTP_404_NOT_FOUND


def exception_handler(response, exc, context) -> Response:
    if response is not None:
        return response
    if isinstance(exc, CustomAPIException):
        return Response(data=APIExceptionSerializer(instance=exc).data, status=exc.status_code)
