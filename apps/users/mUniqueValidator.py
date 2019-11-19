from rest_framework import status
from rest_framework.exceptions import APIException, _get_error_details, ValidationError
from rest_framework.validators import UniqueValidator
from django.db.utils import DataError
from django.utils.translation import gettext_lazy as _

def qs_exists(queryset):
    try:
        return queryset.exists()
    except (TypeError, ValueError, DataError):
        return False


class mValidationError(APIException):
    status_code = status.HTTP_200_OK
    default_detail = _('Invalid input.')
    default_code = 'invalid'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        # For validation failures, we may collect many errors together,
        # so the details should always be coerced to a list if not already.
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]

        self.detail = _get_error_details(detail, code)