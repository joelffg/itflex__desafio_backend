import json
from os import listdir, path

import yaml
from flask import jsonify, request as req

BASE_DOCS_PATH = "/usr/share/doc/itflex/openapi"
SPEC_PATH = "/usr/share/doc/itflex/openapi/openapi.json"
if not path.isdir(BASE_DOCS_PATH):
    BASE_DOCS_PATH = "./docs"
    SPEC_PATH = "./docs/api/spec/openapi.json"


def merge_configs(data, new_data):
    if new_data is None:
        return

    for key, value in new_data.items():
        if key not in data:
            data[key] = value
            continue

        if isinstance(value, dict):
            merge_configs(data[key], value)
            continue
        if isinstance(value, list):
            for item in value:
                data[key].append(item)

            continue


def load_config(config_path, data):
    with open(config_path) as f:
        new_data = yaml.load(f.read(), Loader=yaml.SafeLoader)
        return merge_configs(data, new_data)


def load_dir(dir_path, data, recurse=True):
    if dir_path.rstrip("/").endswith("node_modules"):
        return

    if not path.isdir(dir_path):
        return

    for item_path in sorted(listdir(dir_path)):
        fullpath = path.join(dir_path, item_path)
        if path.isdir(fullpath):
            if recurse:
                load_dir(fullpath, data, recurse=recurse)
            continue

        if not item_path.endswith(".yml"):
            continue

        load_config(fullpath, data)


def load_spec():
    data = {}
    load_dir(BASE_DOCS_PATH, data, recurse=True)

    return data


def load_compiled_spec():
    with open(SPEC_PATH) as f:
        data = f.read()

    return json.loads(data)


def setup_openapi_api(app):
    OPENAPI_DATA = load_compiled_spec()

    @app.route("/api/docs", methods=["GET"])
    def get_openapi_docs():
        idx_path = path.join(BASE_DOCS_PATH, "index.html")
        with open(idx_path) as f:
            return f.read()

    @app.route("/api/spec/openapi.json", methods=["GET"])
    def get_openapi_config():
        data = {**OPENAPI_DATA}
        data["servers"] = [{"url": req.host_url, "description": "Server"}]
        return jsonify(data)

