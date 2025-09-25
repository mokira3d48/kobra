import sys
import traceback
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status

#from apps.base.interfaces.views import exception_handler as base_exception_handler

LOGGER = logging.getLogger(__name__)
DEFAULT_RESPONSE_EXAMPLES = {
    'error': _('An internal server error is occurrence!'),
    'code': 'unknown',
    }


def print_error_traceback() -> None:
    """Printing of details of the error."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_obj = traceback.extract_tb(exc_traceback)
    for o in tb_obj:
        LOGGER.error("\n %16s %8d %64s\n" % (o.name, o.lineno, o.filename,))


def exception_handler_fn(exc, context) -> Response:
    """Function of exception handling in API."""
    response = exception_handler(exc, context)
    # response = base_exception_handler(response, exc, context)
    if response is None:
        # raise exc
        LOGGER.error(str(exc))
        print_error_traceback()
        return Response(
            dict(
                error=DEFAULT_RESPONSE_EXAMPLES['error'],
                message=str(exc), code=DEFAULT_RESPONSE_EXAMPLES['code']
                ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return response
