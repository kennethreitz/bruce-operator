import logme
from requests import Session
import os

from .env import (
    BUILDPACKS_DIR,
    BUILDKIT_TEMPLATE,
    BUILDPACKS_DOWNLOAD_DIR,
    OPERATOR_HTTP_SERVICE_ADDRESS,
)

from . import storage

requests = Session()

# TODO: support builkit versions.

buildpacks = []


@logme.log
class Buildpack:
    def __init__(self, name):
        global buildpacks
        self.name = name
        self.buildkit = None
        self.repo = None
        self.index = None
        self.meta = {}
        self.minio = storage.get_minio()

        # Ensure the buildpacks directory exists.
        os.makedirs(BUILDPACKS_DOWNLOAD_DIR, exist_ok=True)

        # Install buildpack into global dictionary.
        buildpacks.append(self)

    @property
    def is_repo(self):
        return bool(self.repo)

    def _download_url_to_minio(self, url, f_name):
        self.logger.info(f"Downloading {self.name!r} buildpack...")
        r = requests.get(url)
        storage.set_buildpack(minio=self.minio, name=f_name, value=r.content)

    def _f_name(self, i):
        i = i = "%03d" % i
        return f"{i}-{self.name}.tgz"

    def fetch_repo(self, i=0):
        is_github = "github.com" in self.repo

        cached_buildpack = storage.get_buildpack(minio=self.minio, name=self._f_name(i))
        if not cached_buildpack:
            if is_github:
                url = f"{self.repo}/archive/master.tar.gz"
                self._download_url_to_minio(url=url, f_name=self._f_name(i))

    def fetch_buildkit(self, i=0):
        url = BUILDKIT_TEMPLATE.format(self.buildkit)

        if not os.path.isfile(self._f_name(i)):
            self._download_url_to_minio(url=url, f_name=self._f_name(i))
        else:
            self.logger.info(f"Using cached {self.name!r} buildpack.")

    def fetch(self, i=0):
        if self.is_repo:
            return self.fetch_repo(i)
        else:
            return self.fetch_buildkit(i)

    def __repr__(self):
        return f"<Buildpack name={self.name!r}>"

    @property
    def url(self):
        return f"{OPERATOR_HTTP_SERVICE_ADDRESS}/{self.name}.tgz"

    @classmethod
    def from_info(kls, info):
        self = kls(name=info["metadata"]["name"])
        self.buildkit = info["spec"].get("buildkit")
        self.repo = info["spec"].get("repo")
        self.index = info["spec"].get("index")

        return self


def fetch_buildpack(*, i=0, buildpack_info):
    bp = Buildpack.from_info(buildpack_info)
    bp_path = bp.fetch(i)
    # print(bp_path)
