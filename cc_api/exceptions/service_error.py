from .error_core import ErrorCore
from enum import unique


@unique
class ServiceError(ErrorCore):
    NO_AUTH = 1

    def descriptions(self, error, *context):
        _descriptions = {
            'NO_AUTH': 'Insufficient permissions'
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
