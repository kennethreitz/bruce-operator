"""BRUCE Operator.

Usage:
  bruce-operator watch [--buildpacks|--apps]
  bruce-operator fetch-buildpacks
  bruce-operator http
  bruce-operator (-h | --help)

Options:
  -h --help     Show this screen.
"""

import sys
from docopt import docopt

from .operator import Operator
from .http import app


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

    if args["http"]:
        print("Starting webapp...")
        app.run()


if __name__ == "__main__":
    main()
