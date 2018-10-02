"""BRUCE Operator.

Usage:
  bruce-operator watch [--buildpacks|--apps]
  bruce-operator fetch-buildpacks
  bruce-operator http
  bruce-operator build <appname>
  bruce-operator (-h | --help)

Options:
  -h --help     Show this screen.
"""

import os
import sys

import delegator
from docopt import docopt

from .operator import Operator
from .http import app
from .env import IN_WINDOWS
from .builds import bootstrap_docker


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

        if not IN_WINDOWS:
            os.system("gunicorn bruce_operator.http:app -b 0.0.0.0:80")
        else:
            app.run(port=80)

    if args["build"]:
        app_name = args["<appname>"]
        print(f"Building {app_name}")
        bootstrap_docker()
        operator.build_app(app_name=app_name)


if __name__ == "__main__":
    main()
