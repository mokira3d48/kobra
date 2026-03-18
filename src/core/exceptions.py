import sys
import traceback
import logging
import json

from loguru import logger
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import exception_handler

# from your_app.exceptions import exception_handler as your_app_exception_handler
from v1.container.exceptions import exception_handler as v1_container_exception_handler


class CustomAPIException(APIException):

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
        self.code = code if code is not None else self.__class__.default_code


class CustomAPIExceptionSerializer(serializers.Serializer):
    detail = serializers.JSONField(read_only=True)
    code = serializers.CharField(read_only=True)


def print_error_traceback() -> None:
    """
    Printing of details of the error.
    """
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_obj = traceback.extract_tb(exc_traceback)
    for o in tb_obj:
        logger.error("%16s %8d %64s" % (o.name, o.lineno, o.filename,))


def exception_handler_fn(exc, context):
    """Function of exception handling in API."""
    response = exception_handler(exc, context)
    response = v1_container_exception_handler(response, exc, context)

    if settings.DEBUG:
        print_error_traceback()
    # logger.info("exc: " + str(vars(exc)))
    if response is None:
        exc = CustomAPIException(exc.args, code=exc.__class__.__name__)
        ser = CustomAPIExceptionSerializer(instance=exc)
        return Response(ser.data, status=exc.status_code)
    return response
