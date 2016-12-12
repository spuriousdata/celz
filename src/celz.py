#!/usr/bin/env python3
import sys
from argparse import ArgumentParser
from celz.app import Celz


def main():
    parser = ArgumentParser()
    parser.add_argument('FILE', help='file to open')

    args = parser.parse_args(sys.argv[1:])
    Celz(args.FILE)


if __name__ == '__main__':
    main()
