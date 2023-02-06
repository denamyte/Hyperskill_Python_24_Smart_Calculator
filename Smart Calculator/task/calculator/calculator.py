def main():
    while True:
        match input().strip().split():
            case ['/help']:
                print('The program calculates the sum of numbers')
            case ['/exit']:
                print('Bye!')
                break
            case []:
                continue
            case params:
                print(sum(map(int, params)))


if __name__ == '__main__':
    main()
