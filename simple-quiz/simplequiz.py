from argparse import ArgumentParser

from parse import parse


def main():
    argparser = ArgumentParser()

    argparser.add_argument('file_path')

    args = argparser.parse_args()

    parse(args.file_path)


main()
