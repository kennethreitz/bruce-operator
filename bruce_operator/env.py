import os

WATCH_NAMESPACE = os.environ.get("WATCH_NAMESPACE", "bruce")
API_VERSION = "v1alpha1"
API_GROUP = "bruce.kennethreitz.org"

BUILDPACKS_DIR = "/opt/buildpacks"
APPCACHE_DIR = "/opt/caches"
OPERATOR_IMAGE = "bruceproject/operator:latest"
TOKEN_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/token"
CERT_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
IN_KUBERNETES = os.path.isfile(TOKEN_LOCATION)
KUBECONFIG_PATH = os.path.expanduser("~/.kube/config")
