"""
We want to
    * cache json schemas locally (because speed and behind proxy)
    * deref them into single files

Example:
    assert_url_local("http://swagger.io/v2/schema.json")

"""

import json
from os import makedirs
from os.path import dirname, isfile
from urllib.parse import urljoin, urlsplit

import requests

DATA_DIR = dirname(__file__) + "/source"
ENCODING = "utf-8"


def get_local_path(url):
    url_parts = urlsplit(url)
    path = DATA_DIR + "/" + url_parts.netloc + "/" + url_parts.path
    return path


def assert_url_local(url):
    local_path = get_local_path(url)
    if not isfile(local_path):
        makedirs(dirname(local_path), exist_ok=True)
        print(f"DOWNLOAD: {url}")
        res = requests.get(url)
        res.raise_for_status()
        with open(local_path, "wb") as file:
            file.write(res.content)
    return local_path


def url2json(url):
    with open(assert_url_local(url), "r", encoding=ENCODING) as file:
        return json.load(file)


def load_parse(o, url, base_url=None):
    def x(o: dict):
        res = dict((k, load_parse(v, url, base_url)) for k, v in o.items())
        if "$ref" in res and isinstance(res["$ref"], str):
            if not res["$ref"].startswith("#"):
                res_orig = res
                ref = res_orig.pop("$ref")
                ref_url = urljoin(base_url or url, ref)
                res = url2json(ref_url)
                res = load_parse(res, ref_url, base_url)
                # merge other values(except $ref)
                res.update(res_orig)
            else:
                # local ref
                if not res["$ref"].startswith("#/"):
                    raise NotImplementedError(
                        "relative nested refs not yet implemented"
                    )
        return res

    if isinstance(o, dict):
        return x(o)
    elif isinstance(o, list):
        return [load_parse(v, url, base_url) for v in o]
    else:
        return o


def load(local_path, url, base_url=None):
    if not isfile(local_path):
        makedirs(dirname(local_path), exist_ok=True)
        schema = load_parse({"$ref": url}, url, base_url)
        if "$id" not in schema:
            schema["$id"] = url
        assert schema["$id"] == url
        schema_str = json.dumps(schema, indent=2, ensure_ascii=False, sort_keys=True)
        with open(local_path, "w", encoding=ENCODING) as file:
            file.write(schema_str)
    with open(local_path, "r", encoding=ENCODING) as file:
        return json.load(file)


if __name__ == "__main__":
    for url in [
        "http://swagger.io/v2/schema.json",  # open api 2.0
        "https://spec.openapis.org/oas/3.0/schema/2021-09-28",
        "https://spec.openapis.org/oas/3.1/schema/2022-10-07",
        "https://json-schema.org/draft/2020-12/schema",
        "https://json-schema.org/draft-07/schema",
        "https://raw.githubusercontent.com/frictionlessdata/specs/master/schemas/tabular-data-package.json",
        "https://specs.frictionlessdata.io/schemas/tabular-data-resource.json",
        "https://specs.frictionlessdata.io/schemas/tabular-data-package.json",
    ]:
        assert_url_local(url)