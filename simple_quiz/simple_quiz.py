from argparse import ArgumentParser

import parse
import parse_marko
import parse_mistune


def main():
    argparser = ArgumentParser()

    argparser.add_argument('file_path')
    argparser.add_argument(
        '--parser', choices=['custom', 'marko', 'mistune'],
        default='mistune')

    args = argparser.parse_args()

    if args.parser == 'custom':
        parse.parse(args.file_path)
    elif args.parser == 'marko':
        parse_marko.parse(args.file_path)
    elif args.parser == 'mistune':
        parse_mistune.parse(args.file_path)


main()
