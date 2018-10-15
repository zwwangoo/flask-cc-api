from enum import unique

from .error_core import ErrorCore


@unique
class SystemError(ErrorCore):
    '''
    defined system errors
    '''

    # system level (100xxx)

    SYSTEM_ERROR = 100001
    SERVICE_UNAVAILABLE = 100002
    REMOTE_SERVICE_ERROR = 100003
    LIMITED_IP_ADDRESS = 100004
    PARAM_ERROR = 100005
    TOO_MANY_PENDING_TASKS = 100006
    JOB_EXPIRED = 100007
    RPC_ERROR = 100008
    MISSING_REQUIRED_PARAMETER = 100009
    PARAMETER_VALUE_INVALID = 100010

    MISSING_AUTHORIZATION_HEADER = 101001
    BAD_AUTHORIZATION_HEADER = 101003

    def descriptions(self, error, *context):
        '''
        generate error desc
        :params error: SystemError object
        :returns: description with string for error
        '''

        _descriptions = {
            'SYSTEM_ERROR': 'System error.',
            'SERVICE_UNAVAILABLE': 'System unavailable.',
            'REMOTE_SERVICE_ERROR': 'Remote service error.',
            'LIMITED_IP_ADDRESS': 'Limited IP address.',
            'PARAM_ERROR': 'Limited IP address.',
            'TOO_MANY_PENDING_TASKS': 'Too many pending tasks, system is busy.',
            'JOB_EXPIRED': 'Job expired.',
            'RPC_ERROR': 'RPC error.',
            'MISSING_REQUIRED_PARAMETER': 'Missing required parameter ({}), see docs for more info.',
            'PARAMETER_VALUE_INVALID': 'Parameter ({0})’s value invalid: {0}, see docs for more info.',

            'MISSING_AUTHORIZATION_HEADER': 'Missing authorization header.',
            'BAD_AUTHORIZATION_HEADER': 'Bad Authorization header. Expected value \'Bearer <JWT>\'',
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
