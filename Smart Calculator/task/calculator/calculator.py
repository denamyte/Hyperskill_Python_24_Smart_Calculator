import re
from typing import List
from operator import add, sub, mul, floordiv, pow

import exceptions as ex

RE_INSERT_SPACES = {' + ': re.compile(r'(?<=[\w)])\++(?=[\w(])'),
                    ' - ': re.compile(r'(?<=[\w)])-+(?=[\w(])'),
                    ' * ': re.compile(r'(?<=[\w()])\*(?=[\w()])'),
                    ' / ': re.compile(r'(?<=[\w()])/(?=[\w()])'),
                    ' ^ ': re.compile(r'(?<=[\w()]) *\^ *(?=[\w()])'),
                    ' ( ': re.compile(r' *\( *'),
                    ' ) ': re.compile(r' *\) *')}
RE_PLUSES = re.compile(r'\++$')
RE_MINUSES = re.compile('-+$')
RE_ASSIGNMENT = re.compile(' *= *')
RE_IDENTIFIER = re.compile('[a-zA-Z]+$')
RE_NUMBER = re.compile(r'[+-]*[0-9]+$')
RE_MIXED_IDENT = re.compile('[+-]*([a-zA-Z]+[0-9]+|[0-9]+[a-zA-Z]+)')
RE_WRONG_OPERATOR = re.compile('[/*]{2,}')

OPERATORS = {'+': add,
             '-': sub,
             '*': mul,
             '/': floordiv,
             '^': pow}

var_to_values = {}


def main():
    while True:
        try:
            match insert_spaces(input()).strip():
                case '':
                    continue
                # assignment of a variable
                case s if '=' in s:
                    assign_variable(s)
                # command
                case s if s.startswith('/'):
                    match s:
                        case '/help':
                            print('The program calculates the sum of numbers')
                        case '/exit':
                            print('Bye!')
                            break
                        case _:
                            raise ex.UnknownCmdError()
                # only expression
                case s:
                    print(solv_expr(s))

        except BaseException as e:
            print(e)


def insert_spaces(s: str) -> str:
    for key, pattern in RE_INSERT_SPACES.items():
        s = pattern.sub(key, s)
    return s


def assign_variable(s: str):
    parts = RE_ASSIGNMENT.split(s)
    if not RE_IDENTIFIER.match(parts[0]):
        raise ex.InvIdentError()

    if len(parts) > 2 or any(RE_MIXED_IDENT.match(token) for token
                             in parts[1].split()):
        raise ex.InvAssignmentError()

    var_to_values[parts[0]] = solv_expr(parts[1])


def solv_expr(s: str) -> int:
    tokens = prepare_and_check_tokens(s)
    postfix = to_postfix(tokens)
    return eval_postfix(postfix)


def prepare_and_check_tokens(s: str) -> List[str]:
    tokens = s.split()
    parenthesis_sum = 0
    for i, token in enumerate(tokens):
        match token:
            case t if RE_PLUSES.match(t):
                tokens[i] = '+'
            case t if RE_MINUSES.match(t):
                tokens[i] = '-' if len(t) % 2 else '+'
            case t if RE_MIXED_IDENT.match(t):
                raise ex.InvIdentError()
            case t if t in var_to_values:
                tokens[i] = var_to_values[t]
            case t if t in '()':
                parenthesis_sum += 1 if t == '(' else -1
            case t if RE_IDENTIFIER.match(t):
                # up to this point, all known identifiers are already substituted
                raise ex.UnknownVarError()
            case t if RE_WRONG_OPERATOR.match(t):
                raise ex.InvExprError()
    if parenthesis_sum:
        raise ex.InvExprError()

    return tokens


def to_postfix(expr: List[str]) -> List[str]:
    result = []
    stack: List[str] = []

    for token in expr:
        match token:
            case t if RE_NUMBER.match(t):
                result.append(t)

            case t if t in OPERATORS:
                while True:
                    if not stack or stack[-1] == '(':
                        stack.append(t)
                        break
                    top = stack[-1]

                    t_p = get_precedence(t)
                    top_p = get_precedence(top)
                    if t_p > top_p:
                        stack.append(t)
                        break
                    else:
                        result.append(stack.pop())

            case t if t == '(':
                stack.append(t)

            case t if t == ')':
                pop = stack.pop()

                while pop != '(':
                    result.append(pop)
                    pop = stack.pop()

    while stack:
        result.append(stack.pop())

    return result


def get_precedence(s: str):
    result = 0
    for op in OPERATORS:
        result += 1

        if op == s:
            if op in '-/':
                result -= 1
            break

    return result


def eval_postfix(expr: List[str]) -> int:
    stack = []
    for token in expr:
        if RE_NUMBER.match(token):
            stack.append(token)
        else:
            op = OPERATORS.get(token)
            b = int(stack.pop())
            a = int(stack.pop())
            stack.append(op(a, b))
    return stack[0]


if __name__ == '__main__':
    main()
