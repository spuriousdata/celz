#!/usr/bin/env python3
import sys
import logging
from argparse import ArgumentParser
from celz.app import Celz


def main():
    parser = ArgumentParser()
    parser.add_argument('-v', help='verbosity level', action='count')
    parser.add_argument('-l', help='logfile', default='./celz.log')
    parser.add_argument('FILE', help='file to open')

    args = parser.parse_args(sys.argv[1:])

    ll = logging.ERROR
    if args.v == 1:
        ll = logging.WARNING
    elif args.v == 2:
        ll = logging.INFO
    elif args.v == 3:
        ll = logging.DEBUG

    logging.basicConfig(filename=args.l, level=ll)

    Celz(args.FILE)


if __name__ == '__main__':
    main()
