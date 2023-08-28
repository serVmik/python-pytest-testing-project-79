import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser(
        prog="page-loader",
        description='',
    )
    parser.add_argument('url',
                        type=str,
                        )
    parser.add_argument('-o',
                        '--output',
                        default=os.getcwd(),
                        type=str,
                        )
    args = parser.parse_args()

    return args
