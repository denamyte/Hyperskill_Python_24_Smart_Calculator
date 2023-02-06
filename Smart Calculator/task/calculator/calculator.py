from typing import List

OPS = {'+': 1, '-': -1}


def main():
    while True:
        match split_and_process_signs(input()):
            case ['/help']:
                print('The program calculates the sum of numbers')
            case ['/exit']:
                print('Bye!')
                break
            case tokens if len(tokens):
                res = 0
                sign = 1
                for token in tokens:
                    if token in OPS:
                        sign = OPS[token]
                    else:
                        res += sign * int(token)
                print(res)


def split_and_process_signs(raw: str) -> List[str]:
    """
    Convert '+++...' into a single '+'.

    Convert '---...' into a '-' if raw length is odd, and into a '+', otherwise.
    :param raw: input string
    :return: a list of preprocessed tokens
    """
    tokens = raw.split()
    for i, token in enumerate(tokens):
        match token:
            case t if t.endswith('+'):
                tokens[i] = '+'
            case t if t.endswith('-'):
                tokens[i] = '-' if len(t) % 2 else '+'

    return tokens


if __name__ == '__main__':
    main()
