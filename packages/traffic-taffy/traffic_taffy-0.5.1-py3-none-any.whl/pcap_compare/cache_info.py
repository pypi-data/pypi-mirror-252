"""Loads the cached data for a file to display the results about it"""

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType
from logging import debug, info, warning, error, critical
from rich import print
import logging
import sys
import pickle

def parse_args():
    "Parse the command line arguments."
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter,
                            description=__doc__,
                            epilog="Exmaple Usage: ")

    parser.add_argument("--log-level", "--ll", default="info",
                        help="Define the logging verbosity level (debug, info, warning, error, fotal, critical).")

    parser.add_argument("cache_file", type=str,
                        help="The cache file to load and display information about")

    args = parser.parse_args()
    log_level = args.log_level.upper()
    logging.basicConfig(level=log_level,
                        format="%(levelname)-10s:\t%(message)s")
    return args

def main():
    args = parse_args()
    contents = pickle.load(open(args.cache_file, "rb"))

    # play the major keys
    for key in contents.keys():
        if key != 'dissection' and key != 'parameters':
            print(f"{key:<20} {contents[key]}")

    # then the minors
    print("parameters:")
    for key in contents['parameters']:
        print(f"    {key:<16} {contents['parameters'][key]}")
    
    


if __name__ == "__main__":
    main()
