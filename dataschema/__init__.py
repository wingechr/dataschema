__version__ = "0.0.0"
__appname__ = "dataschema"

import json
from functools import cache
from os import makedirs
from os.path import dirname, isfile, realpath
from urllib.parse import urlsplit

import appdirs
import frictionless
import jsonschema
import requests


def validate_resource(resource_descriptor):
    res = frictionless.Resource(resource_descriptor)
    rep = res.validate()

    if rep.stats["errors"]:
        errors = []
        for task in rep.tasks:
            for err in task["errors"]:
                errors.append(err["message"])

        err_str = "\n".join(errors)
        # logging.error(err_str)
        raise ValueError(err_str)


@cache
def get_cache_dir():
    return appdirs.user_cache_dir(__appname__, appauthor=None, version=None)


@cache
def get_local_path(url, cache_dir=None):
    cache_dir = cache_dir or get_cache_dir() + "/schema"
    url_parts = urlsplit(url)
    path = cache_dir + "/" + url_parts.netloc + "/" + url_parts.path
    return realpath(path)


@cache
def get_jsonschema(schema_url, cache_dir=None, encoding="utf-8"):
    local_path = get_local_path(schema_url, cache_dir=cache_dir)
    if not isfile(local_path):
        makedirs(dirname(local_path), exist_ok=True)
        res = requests.get(schema_url)
        res.raise_for_status()
        res = json.dumps(res.json(), indent=4, ensure_ascii=False)
        with open(local_path, "w", encoding=encoding) as file:
            file.write(res)
    with open(local_path, "r", encoding=encoding) as file:
        return json.load(file)


def get_jsonschema_validator(schema):
    """Return validator instance for schema.

    Example:

    >>> schema = {"type": "object", "properties": {"id": {"type": "integer"}}, "required": [ "id" ]}  # noqa
    >>> validator = get_jsonschema_validator(schema)
    >>> validator({})
    Traceback (most recent call last):
        ...
    ValueError: 'id' is a required property ...

    >>> validator({"id": "a"})
    Traceback (most recent call last):
        ...
    ValueError: 'a' is not of type 'integer' ...

    >>> validator({"id": 1})

    """

    if isinstance(schema, str):
        schema = get_jsonschema(schema)

    validator_cls = jsonschema.validators.validator_for(schema)
    # check if schema is valid
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    def validator_function(instance):
        errors = []
        for err in validator.iter_errors(instance):
            # path in data structure where error occurs
            path = "$" + "/".join(str(x) for x in err.absolute_path)
            errors.append("%s in %s" % (err.message, path))
        if errors:
            err_str = "\n".join(errors)
            # logging.error(err_str)
            raise ValueError(err_str)

    return validator_function
