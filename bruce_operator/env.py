import os

WATCH_NAMESPACE = os.environ.get("WATCH_NAMESPACE", "bruce")
API_VERSION = "v1alpha1"
API_GROUP = "bruce.kennethreitz.org"

OPERATOR_HTTP_SERVICE_ADDRESS = "http://bruce.bruce-operator:80"
REGISTRY_URL = os.environ.get("REGISTY_URL", "localhost:80")
# APPCACHE_DIR = "/opt/caches"
OPERATOR_IMAGE = "kennethreitz/bruce-operator:latest"
TOKEN_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/token"
CERT_LOCATION = "/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
IN_KUBERNETES = os.path.isfile(TOKEN_LOCATION)
IN_WINDOWS = os.name == "nt"
KUBECONFIG_PATH = os.path.expanduser("~/.kube/config")
BUILDKIT_TEMPLATE = "https://codon-buildpacks.s3.amazonaws.com/buildpacks/{}.tgz"

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_SERVER = os.environ.get("MINIO_SERVER")
BUILDPACKS_BUCKET = "buildpacks"

HEROKUISH_IMAGE = "gliderlabs/herokuish"
