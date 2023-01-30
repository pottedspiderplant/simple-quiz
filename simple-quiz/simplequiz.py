from argparse import ArgumentParser

import parse_marko
import parse


def main():
    argparser = ArgumentParser()

    argparser.add_argument('file_path')
    argparser.add_argument('--oldparser', action='store_true')

    args = argparser.parse_args()

    if args.oldparser:
        parse.parse(args.file_path)
    else:
        parse_marko.parse(args.file_path)


main()
