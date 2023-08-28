#!usr/bin/env python3
from page_loader.parse_args import parse_args
from page_loader.pg_loader import download


def main():
    args = parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
