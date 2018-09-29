"""BRUCE Operator.

Usage:
  bruce-operator watch
  bruce-operator (-h | --help)

Options:
  -h --help     Show this screen.
"""

import sys
from docopt import docopt

from .core import watch


def main():
    args = docopt(__doc__)

    if args["watch"]:
        watch()


if __name__ == "__main__":
    main()
