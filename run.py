import sys

def main():
    if len(sys.argv) != 3:
        print('usage: python3 run.py ENCRYPT/DECRYPT "password here"')
        exit(1)
    if sys.argv[1] == 'ENCRYPT':
        pass
    elif sys.argv[1] == 'DECRYPT':
        pass
    else:
        print(f"Unknown option: {sys.argv[1]}")
        print('usage: python3 run.py ENCRYPT/DECRYPT "password here"')

if __name__ == '__main__':
    main()
