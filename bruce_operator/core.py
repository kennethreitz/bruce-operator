import time

import kubernetes
from kubernetes.client.configuration import Configuration
from kubernetes.client.api_client import ApiClient

from .env import WATCH_NAMESPACE


class Operator:
    def __init__(self, api_client=None):
        self.watchers = []
        self.api_client = None

        config = Configuration()
        if api_client:
            self.api_client = api_client
        else:
            if not config.api_client:
                config.api_client = ApiClient()
            self.api_client = config.api_client

    def _build_url(self, api_version, kind, namespace=None):
        resource = self.lookup_resource(api_version, kind)
        if not resource:
            print("ERR", api_version, kind)
            exit

        api_prefix = "api" if api_version == "v1" else "apis"
        if resource["namespaced"] and namespace:
            if not namespace:
                namespace = "default"
            return (
                f"/{api_prefix}/{api_version}/namespaces/{namespace}/{resource['name']}"
            )

        return f"/{api_prefix}/{api_version}/{resource['name']}"

    def register_watcher(self, callback):
        self.watchers.append(callback)

    def watch(self):
        url = self._build_url(api_version="v1", kind="", namespace=WATCH_NAMESPACE)

        w = kubernetes.watch.Watch(return_type=object)
        for event in w.stream(
            self.generic.list_generic, resource_path=url, timeout_seconds=90000
        ):
            for watcher in self.watchers:
                watcher(event)


def app_watcher(event):
    print(event)


def buildpack_watcher(event):
    print(event)


operator = Operator()
operator.register_watcher(app_watcher)
operator.register_watcher(buildpack_watcher)


def watch():
    operator.watch()
