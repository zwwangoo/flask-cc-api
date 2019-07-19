from enum import unique

from .error_core import ErrorCore


@unique
class SystemError(ErrorCore):
    '''
    defined system errors
    '''

    # system level (100xxx)

    SYSTEM_ERROR = 101001
    SERVICE_UNAVAILABLE = 101002
    REMOTE_SERVICE_ERROR = 101003
    TOO_MANY_PENDING_TASKS = 101004
    JOB_EXPIRED = 101005
    RPC_ERROR = 101006
    DATABASE_ERROR = 101007

    MISSING_REQUIRED_PARAMETER = 102001
    PARAMETER_VALUE_INVALID = 102002
    BAD_AUTHORIZATION_HEADER = 102005
    MISSING_AUTHORIZATION_HEADER = 102004
    EXPORED_SIGNATURE_ERROR = 102008
    INVALID_SIGNATURE_ERROR = 102009
    WRONG_TOKEN = 102010
    LIMITED_IP_ADDRESS = 102003

    def descriptions(self, error, *context):
        '''
        generate error desc
        :params error: SystemError object
        :returns: description with string for error
        '''

        _descriptions = {
            'SYSTEM_ERROR': '系统错误',
            'SERVICE_UNAVAILABLE': '服务不可用',
            'REMOTE_SERVICE_ERROR': '远程调用报错',
            'TOO_MANY_PENDING_TASKS': '当前任务过多，系统繁忙',
            'JOB_EXPIRED': '任务超时',
            'RPC_ERROR': 'RPC 错误',
            'DATABASE_ERROR': '数据库错误',

            'MISSING_REQUIRED_PARAMETER': '缺少必要参数({})',
            'PARAMETER_VALUE_INVALID': '参数({})的值是无效的',
            'MISSING_AUTHORIZATION_HEADER': '缺少授权头部',
            'BAD_AUTHORIZATION_HEADER': '授权头部错误, \'Bearer <JWT>\'',
            'LIMITED_IP_ADDRESS': 'IP地址受限',
            'EXPORED_SIGNATURE_ERROR': '签名过期',
            'INVALID_SIGNATURE_ERROR': '签名无效',
            'WRONG_TOKEN': '错误的令牌',
        }

        error_desc = _descriptions[str(error).split('.')[1]]

        if context:
            result = error_desc.format(*context)
            return result

        return error_desc
