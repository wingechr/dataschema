__version__ = "0.0.0"

from functools import cache

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
def get_jsonschema(schema_url):
    return requests.get(schema_url).json()


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
