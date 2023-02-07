import re

import exceptions as ex
import operands as op

RE_PLUSES = re.compile(r'\++$')
RE_MINUSES = re.compile('-+$')
RE_ASSIGNMENT = re.compile(' *= *')
RE_IDENTIFIER = re.compile('[a-zA-Z]+$')
RE_MIXED = re.compile('[+-]*([a-zA-Z]+[0-9]+|[0-9]+[a-zA-Z]+)')

var_to_values = {}


def main():
    while True:
        try:
            match input():
                case '':
                    continue
                case s if '=' in s:  # assignment of a variable
                    assign_variable(s)
                case s if s.startswith('/'):  # command
                    match s:
                        case '/help':
                            print('The program calculates the sum of numbers')
                        case '/exit':
                            print('Bye!')
                            break
                        case _:
                            raise ex.UnknownCmdError()
                case s:  # only expression
                    print(parse_expr(s).result())
        except BaseException as e:
            print(e)


def parse_expr(raw: str) -> op.ExprNode:
    tokens = raw.split()
    expr = op.Operand('')
    for token in tokens:
        match token:
            case t if RE_PLUSES.match(t):
                expr = expr.add_node(op.Operator('+'))
            case t if RE_MINUSES.match(t):
                expr = expr.add_node(op.Operator('-' if len(t) % 2 else '+'))
            case t if RE_MIXED.match(t):
                raise ex.InvIdentError()
            case t if t in var_to_values:
                expr = expr.add_node(op.Operand(var_to_values[t]))
            case t if RE_IDENTIFIER.match(t):
                raise ex.UnknownVarError()
            case t:
                expr = expr.add_node(op.Operand(t))

    return expr


def assign_variable(raw: str):
    parts = RE_ASSIGNMENT.split(raw.strip())
    if not RE_IDENTIFIER.match(parts[0]):
        raise ex.InvIdentError()
    if len(parts) > 2 or any(RE_MIXED.match(token) for token
                             in parts[1].split()):
        raise ex.InvAssignmentError()
    var_to_values[parts[0]] = parse_expr(parts[1]).result()


if __name__ == '__main__':
    main()
