from operator import add, sub
from abc import abstractmethod, ABC
from dataclasses import dataclass
from exceptions import InvExprError

OPERATORS = {'+': add,
             '-': sub}


@dataclass
class ExprNode(ABC):
    _value: str

    def add_node(self, other: 'ExprNode') -> 'ExprNode':
        match self, other:
            case (ExprNode(_value=''), that):  # start case
                return that
            case (this, Operator() as that):
                that.left = this
                return that
            case (Operator() as this, that):
                this.right = that
                return this
        raise InvExprError()

    @abstractmethod
    def result(self) -> int:
        pass


class Operand(ExprNode):
    def result(self) -> int:
        try:
            return int(self._value)
        except ValueError:
            raise InvExprError()

    def __str__(self):
        return self._value


@dataclass
class Operator(ExprNode):
    left: ExprNode = None
    right: ExprNode = None

    def result(self) -> int:
        return OPERATORS[self._value](self.left.result(), self.right.result())

    def __str__(self):
        return f'{self.left} {self._value} {self.right}'
