import os
import time
import json
from uuid import uuid4
from functools import lru_cache

import logme
import kubernetes
import delegator
from kubeconfig import KubeConfig
from kubernetes.client.configuration import Configuration
from kubernetes.client.api_client import ApiClient

from .env import (
    WATCH_NAMESPACE,
    API_GROUP,
    API_VERSION,
    OPERATOR_IMAGE,
    KUBECONFIG_PATH,
    IN_KUBERNETES,
    CERT_LOCATION,
    TOKEN_LOCATION,
)
from .kubectl import kubectl
from .buildpacks import fetch_buildpack

# https://github.com/kubernetes-client/python/blob/master/examples/create_thirdparty_resource.md


@logme.log
class Operator:
    def __init__(self, api_client=None, fetch_buildpacks=True):

        # Ensure that we can load the kubeconfig.
        self.ensure_kubeconfig()

        # Load Kube configuration into module (ugh).
        kubernetes.config.load_kube_config()

        # Setup clients.
        self.client = kubernetes.client.CoreV1Api()
        self.custom_client = kubernetes.client.CustomObjectsApi(self.client.api_client)

        # Fetch all the buildpacks.
        if fetch_buildpacks:
            self.fetch_buildpacks()

    def installed_buildpacks(self, watch=False):

        group = API_GROUP  # str | The custom resource's group name
        version = API_VERSION  # str | The custom resource's version
        namespace = WATCH_NAMESPACE  # str | The custom resource's namespace
        plural = (
            "buildpacks"
        )  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
        pretty = (
            "true"
        )  # str | If 'true', then the output is pretty printed. (optional)
        watch = (
            watch
        )  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. (optional)

        try:
            api_response = self.custom_client.list_namespaced_custom_object(
                group, version, namespace, plural, pretty=pretty, watch=watch
            )
            for item in api_response["items"]:
                yield item
        except kubernetes.client.rest.ApiException:
            return None

    def installed_apps(self):
        group = "bruce.kennethreitz.org"  # str | The custom resource's group name
        version = "v1alpha1"  # str | The custom resource's version
        namespace = WATCH_NAMESPACE  # str | The custom resource's namespace
        plural = (
            "apps"
        )  # str | The custom resource's plural name. For TPRs this would be lowercase plural kind.
        pretty = (
            "true"
        )  # str | If 'true', then the output is pretty printed. (optional)
        watch = (
            False
        )  # bool | Watch for changes to the described resources and return them as a stream of add, update, and remove notifications. (optional)

        try:
            api_response = self.custom_client.list_namespaced_custom_object(
                group, version, namespace, plural, pretty=pretty, watch=watch
            )
            return api_response["items"]
        except kubernetes.client.rest.ApiException:
            return None

    def kube_spawn_self(self, cmd, label, env=None):
        if env is None:
            env = {}

        # TODO: ENV
        _hash = uuid4().hex
        return kubectl(
            f"run bruce-operator-{label}-{_hash} --image={OPERATOR_IMAGE} -n {WATCH_NAMESPACE} --restart=Never --quiet=True --record=True --image-pull-policy=Always -- bruce-operator {cmd}"
        )

    def spawn_self(self, cmd, label, env=None):
        if env is None:
            env = {}

        # TODO: ENV
        return delegator.run(f"bruce-operator {cmd}", block=False)

    def ensure_kubeconfig(self):
        """Ensures that ~/.kube/config exists, when running in Kubernetes."""
        # If we're running in a kubernets cluster...
        if IN_KUBERNETES:
            host = os.environ["KUBERNETES_SERVICE_HOST"]
            port = os.environ["KUBERNETES_SERVICE_PORT"]
            # Create a KubeConfig file.
            kc = KubeConfig()

            # Read in the secret token.
            with open(TOKEN_LOCATION, "r") as f:
                token = f.read()

            # Set the credentials.
            kc.set_credentials(name="child", token=token)
            # Set the cluster information.
            kc.set_cluster(
                name="parent",
                server=f"https://{host}:{port}",
                certificate_authority=CERT_LOCATION,
            )
            # Set the context.
            kc.set_context(name="context", cluster="parent", user="child")
            # Use the context.
            kc.use_context("context")

    def fetch_buildpacks(self):
        for buildpack_info in self.installed_buildpacks():
            fetch_buildpack(buildpack_info)

    def watch(self, fork=True, buildpacks=False, apps=False):
        if buildpacks and apps:
            raise RuntimeError("Can only watch one at a time: buildpacks and apps.")

        if fork:
            subprocesses = []

            for t in ("apps", "buildpacks"):
                cmd = f"bruce-operator watch --{t}"
                self.logger.info(f"Running $ {cmd} in the background.")
                c = delegator.run(cmd, block=False)
                subprocesses.append(c)

            self.logger.info(f"Blocking on subprocesses completion.")
            for subprocess in subprocesses:
                subprocess.block()
