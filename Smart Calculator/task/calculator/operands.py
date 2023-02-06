from operator import add, sub
from abc import abstractmethod
from dataclasses import dataclass
from exceptions import InvExprError

OPERATORS = {'+': add,
             '-': sub}


@dataclass
class ExprNode:
    value: str

    def add_node(self, other: 'ExprNode') -> 'ExprNode':
        match self, other:
            case (ExprNode(value=''), that):  # start case
                return that
            case (this, Operator() as that):
                that.left = this
                return that
            case (Operator() as this, that):
                this.right = that
                return this
        raise InvExprError()

    @abstractmethod
    def get_result(self) -> int:
        pass


@dataclass
class Operand(ExprNode):
    def get_result(self) -> int:
        try:
            return int(self.value)
        except ValueError:
            raise InvExprError()

    def __str__(self):
        return self.value


@dataclass
class Operator(ExprNode):
    left: 'ExprNode' = None
    right: 'ExprNode' = None

    def get_result(self) -> int:
        return OPERATORS[self.value](self.left.get_result(), self.right.get_result())

    def __str__(self):
        return f'{self.left} {self.value} {self.right}'
