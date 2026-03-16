import sys
import traceback
import json

from loguru import logger
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import exception_handler

# from your_app.exceptions import exception_handler as your_app_exception_handler


class APIExceptionSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)


def print_error_traceback():
    """Printing of details of the error."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_obj = traceback.extract_tb(exc_traceback)
    for o in tb_obj:
        logger.error("%16s %8d %64s" % (o.name, o.lineno, o.filename,))


def exception_handler_fn(exc, context):
    """Function of exception handling in API."""
    response = exception_handler(exc, context)
    # response = your_app_exception_handler(response, exc, context)

    if settings.DEBUG:
        print_error_traceback()

    if response is None:
        if isinstance(exc, APIException):
            if isinstance(exc.detail, (list, dict)):
                exc.detail = json.dumps(exc.detail, indent=4)
            else:
                exc.detail = str(exc.detail)
            response = Response(APIExceptionSerializer(instance=exc).data, status=exc.status_code)
        else:
            if getattr(settings, 'DEBUG') is True:
                response = Response(
                    APIExceptionSerializer(instance=exc).data,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    return response
