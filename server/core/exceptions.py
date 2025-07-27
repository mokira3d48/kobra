import sys
import traceback
import logging

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import status


LOGGER = logging.getLogger(__name__)
DEFAULT_RESPONSE_EXAMPLES = {
    'error': _('An internal server error is occurrence!'),
    'details': _("Exception to string..."),
    'code': 'unknown',
}


class PaymentRequiredException(APIException):
    status_code = 402
    default_detail = _("This action or access required a payment.")
    default_code = 'payment_required'


def print_error_traceback():
    """Printing of details of the error."""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    tb_obj = traceback.extract_tb(exc_traceback)
    for o in tb_obj:
        LOGGER.error("\n\t%16s %8d %64s\n" % (o.name, o.lineno, o.filename,))


def exception_handler_fn(exc, context):
    """Function of exception handling in API."""
    response = exception_handler(exc, context)
    if response is None:
        # raise exc
        LOGGER.error(str(exc))
        print_error_traceback()
        return Response(
            dict(
                error=DEFAULT_RESPONSE_EXAMPLES['error'],
                details=str(exc),
                code=DEFAULT_RESPONSE_EXAMPLES['code']
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
