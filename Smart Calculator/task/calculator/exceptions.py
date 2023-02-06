class UnknownCmdError(BaseException):
    def __str__(self):
        return 'Unknown command'


class InvExprError(BaseException):
    def __str__(self):
        return 'Invalid expression'
