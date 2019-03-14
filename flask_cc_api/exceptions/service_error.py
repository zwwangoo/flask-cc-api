from enum import unique

from .error_core import ErrorCore


@unique
class ServiceError(ErrorCore):
    NO_AUTH = 200001
    INVALID_VALUE = 201006

    def descriptions(self, error, *context):
        _descriptions = {
            'NO_AUTH': 'Insufficient permissions',
            'INVALID_VALUE': 'The parameter ({}) value is invalid',
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
