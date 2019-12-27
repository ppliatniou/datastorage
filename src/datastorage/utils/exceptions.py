from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT


class DetailedValidationError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = 'Invalid data.'
    default_code = 'invalid'


class ConflictError(APIException):
    status_code = HTTP_409_CONFLICT
    default_detail = 'Conflict'
    default_code = 'conflict'


class RegistryError(Exception):
    pass


class LockedStorageError(Exception):
    pass

