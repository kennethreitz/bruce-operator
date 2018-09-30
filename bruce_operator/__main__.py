"""BRUCE Operator.

Usage:
  bruce-operator watch [--buildpacks|--apps]
  bruce-operator fetch-buildpacks
  bruce-operator (-h | --help)

Options:
  -h --help     Show this screen.
"""

import sys
from docopt import docopt

from .operator import Operator


def main():
    args = docopt(__doc__)
    operator = Operator()

    if args["watch"]:
        if args["--buildpacks"]:
            operator.watch(buildpacks=True)
        if args["--apps"]:
            operator.watch(apps=True)

        operator.watch(fork=True)

    if args["fetch-buildpacks"]:
        print("Fetching buildpacks...")
        operator.fetch_buildpacks()


if __name__ == "__main__":
    main()
