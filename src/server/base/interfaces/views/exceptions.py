import typing as tp
from rest_framework.exceptions import *  # noqa
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    HTTP_429_TOO_MANY_REQUESTS,
)

from ..serializers import (
    APIExceptionSerializer
)

SERIALIZER_CLASSES = {
    'ParseError': (APIExceptionSerializer, HTTP_400_BAD_REQUEST),
    'ValidationError': (APIExceptionSerializer, HTTP_400_BAD_REQUEST),
    'AuthenticationFailed': (APIExceptionSerializer, HTTP_401_UNAUTHORIZED),
    'NotAuthenticated': (APIExceptionSerializer, HTTP_401_UNAUTHORIZED),
    'PermissionDenied': (APIExceptionSerializer, HTTP_403_FORBIDDEN),
    'NotFound': (APIExceptionSerializer, HTTP_404_NOT_FOUND),
    'MethodNotAllowed': (APIExceptionSerializer, HTTP_405_METHOD_NOT_ALLOWED),
    'NotAcceptable': (APIExceptionSerializer, HTTP_406_NOT_ACCEPTABLE),
    'UnsupportedMediaType': (APIExceptionSerializer, HTTP_415_UNSUPPORTED_MEDIA_TYPE),
    'Throttled': (APIExceptionSerializer, HTTP_429_TOO_MANY_REQUESTS),
}


def _make_response(
    previous_res: tp.Optional[Response],
    exc: Exception,
    exception_class: type,
) -> tp.Optional[Response]:
    """
    This function allow to make response if the exc is instance
    of exception_class.
    """
    if previous_res is not None:
        return previous_res
    if isinstance(exc, exception_class):
        exception_class_name = exception_class.__name__
        serializer_cls, code = SERIALIZER_CLASSES[exception_class_name]
        return Response(data=serializer_cls(exc).data, status=code)


def exception_handler(
    response: tp.Optional[Response],
    exc: Exception,
    _context: object
) -> tp.Optional[Response]:
    """
    Function of exception handler.
    """
    if response is not None:
        return response
    res = None

    res = _make_response(res, exc, ParseError)
    res = _make_response(res, exc, ValidationError)
    res = _make_response(res, exc, AuthenticationFailed)
    res = _make_response(res, exc, NotAuthenticated)
    res = _make_response(res, exc, PermissionDenied)
    res = _make_response(res, exc, NotFound)
    res = _make_response(res, exc, MethodNotAllowed)
    res = _make_response(res, exc, NotAcceptable)
    res = _make_response(res, exc, UnsupportedMediaType)
    res = _make_response(res, exc, Throttled)
    return res
