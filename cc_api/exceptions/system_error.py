from enum import unique

from .error_core import ErrorCore


@unique
class SystemError(ErrorCore):
    '''
    defined system errors
    '''

    # system level (100xxx)
    SYSTEM_ERROR = 100000
    CANNOT_FIND_APP = 100001

    # service level (110xxx)
    INVALID_PARAMETER = 110000
    INVALID_PARAMETERS = 110001
    MISSING_REQUIRED_PARAMETER = 110002
    MISSING_PARAMETERS = 110003
    PAGE_OUT_OF_RANGE = 110004

    def descriptions(self, error, *context):
        '''
        generate error desc
        :params error: SystemError object
        :returns: description with string for error
        '''

        _descriptions = {
            'SYSTEM_ERROR': 'System error',
            'CANNOT_FIND_APP': 'Can\'t find flask app',
            'INVALID_PARAMETER': 'Parameter value invalid, you provided [{}] for parameter [{}].',
            'INVALID_PARAMETERS': 'Parameter value invalid, {}.',
            'MISSING_REQUIRED_PARAMETER': 'Missing required parameter: {}',
            'MISSING_PARAMETERS': 'Missing parameters, check your request please.',
            'PAGE_OUT_OF_RANGE': 'The page you request is out of range'
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
