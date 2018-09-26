from enum import Enum


class CrabException(Exception):
    pass


class ErrorCore(Enum):
    '''
    abstract class for error enums
    '''

    def descriptions(self, error):
        raise NotImplementedError()

    @property
    def desc(self):
        '''
        return enum desc for error
        '''
        return self.descriptions(self)

    def desc_with_param(self, *context):
        return self.descriptions(self, *context)
