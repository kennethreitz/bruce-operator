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

from .core import watch


def main():
    args = docopt(__doc__)

    if args["watch"]:
        if args["--buildpacks"]:
            watch(buildpacks=True)
        if args["--apps"]:
            watch(apps=True)

        watch(fork=True)

    if args["fetch-buildpacks"]:
        print("fetching")
        exit()


if __name__ == "__main__":
    main()
