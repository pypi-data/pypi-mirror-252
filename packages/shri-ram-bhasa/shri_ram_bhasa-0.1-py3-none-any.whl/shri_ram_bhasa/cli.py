import argparse
from .ramji import run_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    run_file(args.filename)

if __name__ == '__main__':
    main()