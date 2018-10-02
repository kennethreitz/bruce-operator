import os
import uuid
import tempfile
import json
import time
from shutil import rmtree
from pathlib import Path

import delegator

# import docker as docker_api
import logme

# from .db import db
from .env import HEROKUISH_IMAGE, REGISTRY_URL

OUR_HEROKUISH_IMAGE = f"{REGISTRY_URL}/herokuish"


# Run Docker service.
# delegator.run("service docker start")
@logme.log
def bootstrap_docker(logger=None, mirror_herokuish=True):

    # logger.debug("Configuring docker service to allow our insecure registry...")
    # Configure our registry as insecure.
    try:
        with open("/etc/docker/daemon.json", "w") as f:
            data = {"insecure-registries": [REGISTRY_URL]}
            json.dump(data, f)
    # This fails when running on Windows...
    except FileNotFoundError:
        pass

    # logger.info("Starting docker service...")
    delegator.run("service docker start")
    time.sleep(2)

    docker_running = delegator.run("docker ps").ok

    if not docker_running:
        # logger.info("Assuming docker is not available...")
        pass

    else:
        logger.info("Docker started!")
        if mirror_herokuish:
            logger.info("Checking for mirrored Herokuish image...")
            pull = delegator.run(f"docker pull {OUR_HEROKUISH_IMAGE}")
            if not pull.ok:
                logger.debug(pull.out)

                logger.info("Pulling official Herokuish image...")
                delegator.run(f"docker pull {HEROKUISH_IMAGE}")

                logger.info("Pushing Herokuish image to our registry...")
                tag = delegator.run(
                    f"docker tag {HEROKUISH_IMAGE} {OUR_HEROKUISH_IMAGE}"
                )
                assert tag.ok

                push = delegator.run(f"docker push {OUR_HEROKUISH_IMAGE}")
                assert push.ok
            else:
                logger.info("Herokuish is mirrored and up-to-date!")


@logme.log
class BaseBuild:
    def __init__(self):
        self.uuid = uuid.uuid4().hex
        self.paths = {}
        for name in ("cache", "import"):
            self.paths[name] = tempfile.mkdtemp(prefix=f"build-{self.uuid}-{name}-")
        self.repo_url = None

    @property
    def build_name(self):
        return f"build-{self.uuid}"

    @property
    def service_name(self):
        return self.uuid

    def clone(self, repo_url):
        cmd = f"git clone {repo_url} {self.paths['import']}"
        self.logger.debug(f"build {self.uuid!r}: Running $ {cmd}.")

        c = delegator.run(cmd)
        if not c.ok:
            self.logger.warning(
                f"build {self.uuid!r}: The clone of {repo_url!r} failed!"
            )
            self.logger.warning(f"build {self.uuid!r}: {c.err}")
            raise RuntimeError("The clone failed!")
        self.repo_url = repo_url


@logme.log
class Build(BaseBuild):
    def __init__(self, repo_url, app_name, buildpacks_dir):

        super().__init__()
        self.clone(repo_url=repo_url)
        self.app_name = app_name
        self.paths["buildpacks"] = buildpacks_dir
        # self.timeout = HEROUISH_TIMEOUT

    @property
    def has_dockerfile(self):
        assert self.repo_url
        return os.path.isfile((Path(self.paths["import"]) / "Dockerfile").resolve())

    def docker(self, cmd, assert_ok=True, fail=True):
        cmd = f"docker {cmd}"
        self.logger.debug(f"$ {cmd}")
        c = delegator.run(cmd)
        try:
            assert c.ok
        except AssertionError as e:
            self.logger.debug(c.out)
            self.logger.debug(c.err)

            if fail:
                raise e

        return c

    # Inspiration:
    # https://raw.githubusercontent.com/gitlabhq/gitlabhq/04845fdeae75ba5de7c93992a5d55663edf647e0/vendor/gitlab-ci-yml/Auto-DevOps.gitlab-ci.yml
    def build(self, push=True, promote=None):

        # Mark build as started in database.
        # db.start_build(uuid=self.uuid, app_name=self.app_name, repo_url=self.repo_url)

        assert self.repo_url
        docker_cmd = (
            f"run -i --name={self.build_name} -v {self.paths['import']}:/tmp/app -v {self.paths['buildpacks']}:/tmp/buildpacks"
            f" {OUR_HEROKUISH_IMAGE} /bin/herokuish buildpack build"
        )
        build = self.docker(docker_cmd, fail=False)
        self.logger.debug(build.out)
        if not build.ok:
            self.logger.info(f"Build {self.uuid} failed!")

            # Mark build as failed in database.
            # db.fail_build(uuid=self.uuid)

            return build

        # Commit to Docker.
        docker_cmd = f"commit {self.build_name}"
        commit = self.docker(docker_cmd)
        commit_output = commit.out.strip()

        # Create runnable container in docker.
        docker_cmd = (
            f"create --expose 80 --env PORT=80 "
            f"--name={self.service_name} {commit_output} /bin/herokuish procfile start web"
        )
        create = self.docker(docker_cmd)
        create_output = create.out.strip()
        self.logger.debug(create_output)

        # Commit to Docker.
        docker_cmd = f"commit {self.service_name}"
        commit = self.docker(docker_cmd)
        commit_output = commit.out.strip()

        tag_name = f"{REGISTRY_URL}/{self.app_name}/{self.service_name}"
        docker_cmd = f"tag {commit_output} {tag_name}"

        tag = self.docker(docker_cmd)
        tag_output = tag.out.strip()

        if push:
            self.logger.info(f"Pushing build {self.uuid!r} to registry...")
            docker_cmd = f"push {tag_name}"
            push = self.docker(docker_cmd)
            pass

        # Mark build as finished in database.
        # db.succeed_build(uuid=self.uuid)
        if promote:
            self.logger.info(f"Promoting {self.app_name}'s' {promote} to: {self.uuid}.")
            # db.promote_build(app_name=self.app_name, uuid=self.uuid, target=promote)
        return build

    def cleanup(self):
        for name, path in self.paths.items():
            self.logger.info(f"Cleaning up {name}: {path!r}.")
            try:
                rmtree(path)
            except FileNotFoundError:
                pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.cleanup()
