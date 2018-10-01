import os

WATCH_NAMESPACE = os.environ.get("WATCH_NAMESPACE", "bruce")
API_VERSION = "v1alpha1"
API_GROUP = "bruce.kennethreitz.org"

# BUILDPACKS_DIR = "/tmp/buildpacks"
BUILDPACKS_DIR = os.path.expanduser("~/.bruce/buildpacks")
BUILDPACKS_DOWNLOAD_DIR = os.path.expanduser("~/.bruce/buildpacks/.dl")
OPERATOR_HTTP_SERVICE_ADDRESS = "http://bruce.bruce-operator:80"

# APPCACHE_DIR = "/opt/caches"
OPERATOR_IMAGE = "kennethreitz/bruce-operator:latest"
TOKEN_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/token"
CERT_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
IN_KUBERNETES = os.path.isfile(TOKEN_LOCATION)
KUBECONFIG_PATH = os.path.expanduser("~/.kube/config")
BUILDKIT_TEMPLATE = "https://codon-buildpacks.s3.amazonaws.com/buildpacks/{}.tgz"
