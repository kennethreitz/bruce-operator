import logme
from requests import Session
import os

from .env import BUILDPACKS_DIR, BUILDKIT_TEMPLATE

requests = Session()


@logme.log
class Buildpack:
    def __init__(self):
        self.name = None
        self.buildkit = None
        self.repo = None
        self.meta = {}

    @property
    def is_repo(self):
        return bool(self.repo)

    def fetch_repo(self):
        pass

    def fetch_buildkit(self):
        url = BUILDKIT_TEMPLATE.format(self.buildkit)
        f_name = f"{BUILDPACKS_DIR}/{self.name}.tgz"

        if not os.path.isfile(f_name):
            self.logger.info(f"Downloading {self.name!r} buildpack...")

            r = requests.get(url)
            with open(f_name, "wb") as f:
                f.write(r.content)

        return f_name

    def fetch(self):
        if self.is_repo:
            return self.fetch_repo()
        else:
            return self.fetch_buildkit()

    def __repr__(self):
        return f"<Buildpack name={self.name!r}>"

    @classmethod
    def from_info(kls, info):
        self = kls()

        self.name = info["metadata"]["name"]
        self.buildkit = info["spec"].get("buildkit")
        self.repo = info["spec"].get("repo")

        return self


def fetch_buildpack(buildpack_info):
    bp = Buildpack.from_info(buildpack_info)
    bp_path = bp.fetch()
    print(bp_path)
