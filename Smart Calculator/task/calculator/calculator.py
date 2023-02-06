import re
import exceptions as ex
import operands as op

RE_PLUSES = re.compile(r'\++$')
RE_MINUSES = re.compile('-+$')
OPS = {'+': 1, '-': -1}


def main():
    while True:
        try:
            match input():
                case '':
                    continue
                case s if s.startswith('/'):
                    match s:
                        case '/help':
                            print('The program calculates the sum of numbers')
                        case '/exit':
                            print('Bye!')
                            break
                        case _:
                            raise ex.UnknownCmdError()
                case s:
                    expr = parse_expr(s)
                    print(expr.get_result())
        except BaseException as e:
            print(e)


def parse_expr(raw: str) -> op.ExprNode:
    tokens = raw.split()
    expr = op.ExprNode('')
    for token in tokens:
        match token:
            case t if RE_PLUSES.match(t):
                expr = expr.add_node(op.Operator('+'))
            case t if RE_MINUSES.match(t):
                expr = expr.add_node(op.Operator('-' if len(t) % 2 else '+'))
            case t:
                expr = expr.add_node(op.Operand(t))

    return expr


if __name__ == '__main__':
    main()
