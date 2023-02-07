class UnknownCmdError(BaseException):
    def __str__(self):
        return 'Unknown command'


class InvExprError(BaseException):
    def __str__(self):
        return 'Invalid expression'


class InvIdentError(BaseException):
    def __str__(self):
        return 'Invalid identifier'


class InvAssignmentError(BaseException):
    def __str__(self):
        return 'Invalid assignment'


class UnknownVarError(BaseException):
    def __str__(self):
        return 'Unknown variable'
