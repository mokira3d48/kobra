import logging

from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework import serializers
from rest_framework import status


LOG = logging.getLogger(__name__)
DEFAULT_RESPONSE_EXAMPLES = {
    403: {"details": _("Authentication credentials were not provided.")},
    500: {
            'error': _('An internal server error is occurrence!'),
            'details': _("Exception to string..."),
            'code': 'unknown',
        },
}


class BadRequestException(serializers.ValidationError):
    status_code = 400
    default_detail = _("A value of a field is not valid.")
    default_code = 'bad_request'


class CustomizedAPIException(APIException):
    ...


class UnauthorizedException(CustomizedAPIException):
    status_code = 401
    default_detail = _("This user is unauthorized")
    default_code = 'unauthorized'


class PaymentRequiredException(CustomizedAPIException):
    status_code = 402
    default_detail = _("This action or access required a payment.")
    default_code = 'payment_required'


class ForbiddenException(CustomizedAPIException):
    status_code = 403
    default_detail = _("This action or access is forbidden.")
    default_code = 'forbidden'


class NotFoundException(CustomizedAPIException):
    status_code = 404
    default_detail = _("The resource is not found.")
    default_code = 'not_found'


class InternalError(CustomizedAPIException):
    status_code = 500
    default_detail = _("An error is occurrence in the server")
    default_code = 'internal_error'


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = _("The service is not available for the moment.")
    default_code = 'service_unavailable'


class APIExceptionSerializer(serializers.Serializer):
    """Serializer of API error"""

    details = serializers.CharField(read_only=True,
                                    default=_('Something wrong!'))
    code = serializers.CharField(read_only=True, default='error_code')


def exception_handler_fn(exc, context):
    """Function of exception handling in API"""
    response = exception_handler(exc, context)

    # Gérer les exceptions personnalisées
    # if isinstance(exc, CustomBadRequest):
    #     return Response({
    #         'error': exc.detail,
    #         'code': exc.default_code
    #     }, status=exc.status_code)
    #
    # if isinstance(exc, CustomNotFound):
    #     return Response({
    #         'error': exc.detail,
    #         'code': exc.default_code
    #     }, status=exc.status_code)
    if isinstance(exc, serializers.ValidationError):
        # response = APIExceptionSerializer(
        #     {
        #         **exc.detail,
        #         'code': exc.default_code
        #     }
        # )
        # LOG.debug(exc.detail)
        return Response(exc.detail, status=exc.status_code)

    if isinstance(exc, CustomizedAPIException):
        serialized = APIExceptionSerializer(
            {
                'details': exc.detail,
                'code': exc.default_code
            }
        )
        return Response(serialized.data, status=exc.status_code)

    if response is None:
        raise exc
        return Response({
            'error': DEFAULT_RESPONSE_EXAMPLES[500]['error'],
            'details': str(exc),
            'code': DEFAULT_RESPONSE_EXAMPLES[500]['code'],
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
