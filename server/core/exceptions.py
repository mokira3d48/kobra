import sys
import traceback
import logging
import json

from django.utils.translation import gettext_lazy as _
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import exception_handler

# from your_app.exceptions import exception_handler as your_app_exception_handler


LOGGER = logging.getLogger(__name__)


class APIExceptionSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)


def print_error_traceback():
    """Printing of details of the error."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_obj = traceback.extract_tb(exc_traceback)
    for o in tb_obj:
        LOGGER.error("%16s %8d %64s" % (o.name, o.lineno, o.filename,))


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
            response_ser = APIExceptionSerializer(instance=exc)
            response = Response(response_ser.data, status=exc.status_code)

    return response

