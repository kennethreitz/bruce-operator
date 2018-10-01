import jsonpickle
from flask import Flask, jsonify

from .buildpacks import buildpacks
from .operator import Operator

app = Flask(__name__)
operator = Operator()


@app.route("/")
def get_buildpacks():
    bps = {}
    for buildpack in buildpacks:
        bp = {}

        bp["name"] = buildpack.name
        bp["index"] = buildpack.index
        bp["buildkit"] = buildpack.buildkit
        bp["repo"] = buildpack.repo
        bp["url"] = buildpack.url

        bps[buildpack.name] = bp

    return jsonify({"buildpacks": bps})
