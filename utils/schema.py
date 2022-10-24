import json
import logging  # noqa
import os
import re

import jsonref
from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    UniqueConstraint,
    create_engine,
    dialects,
    types,
)


def get_type_cls(name, dialect=None):
    # special cases
    if dialect and dialect.name == "mssql" and name == "BOOLEAN":
        return dialects.mssql.BIT
    return getattr(types, name)


def parse_type(type_str, dialect=None):
    type_str = type_str.upper().replace(" ", "")
    m = re.match(r"^([A-Z0-9]+)(|\(.*\))$", type_str)
    name, args = m.groups()
    args = [int(x) for x in args.replace("(", "").replace(")", "").split(",") if x]
    cls = get_type_cls(name, dialect=dialect)
    inst = cls(*args)
    return inst


def get_attr(data, name, default=None):
    if not isinstance(data, dict):
        return default
    return data.get(name, default)


def context_exception(fun):
    def fun_(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except Exception as exc:
            raise Exception(exc, args, kwargs)

    return fun_


@context_exception
def get_column(data, dialect=None):
    args = []
    kwargs = {}
    name = data["name"]
    name = validate_name(name)
    args.append(name)
    args.append(parse_type(data["type"], dialect=dialect))
    kwargs["comment"] = get_attr(data, "description")
    kwargs["nullable"] = get_attr(data, "nullable", True)
    col = Column(*args, **kwargs)
    return col


def make_field_list(data, default=None):
    if isinstance(data, str):  # one field
        return [data]
    elif isinstance(data, list):  # multiple fields as string
        return data
    else:
        return make_field_list(data.get("fields", default))


def get_pk(data):
    name = get_attr(data, "name")
    fields = make_field_list(data)
    return PrimaryKeyConstraint(*fields, name=name)


def get_uq(data):
    name = get_attr(data, "name")
    fields = make_field_list(data)
    return UniqueConstraint(*fields, name=name)


def get_fk(data):
    name = get_attr(data, "name")
    fields = make_field_list(data)
    reference = data["reference"]
    if isinstance(reference, str):
        reference = {"resource": reference}
    ref_tab = reference["resource"]
    refcolumns = [f"{ref_tab}.{c}" for c in make_field_list(reference, default=fields)]

    return ForeignKeyConstraint(fields, refcolumns=refcolumns, name=name)


def get_field_constraints(field):
    constraints = []
    if field.get("primaryKey"):
        constraints.append(get_pk(field["name"]))
    if field.get("uniqueKey"):
        constraints.append(get_uq(field["name"]))
    if field.get("foreignKey"):
        data = field["foreignKey"].copy()
        data["fields"] = field["name"]
        constraints.append(get_fk(data))
    return constraints


def validate_name(name):
    if not re.match("^[a-z][a-z0-9_]{2,63}$", name):
        logging.warning(f"invalid name: {name}")
    return name


def get_tab(data, meta):
    dialect = meta.bind.dialect
    name = data["name"]
    name = validate_name(name)
    schema_name = data.get("schemaName")
    description = get_attr(data, "description")
    table_schema = data["schema"]
    columns = [get_column(c, dialect=dialect) for c in table_schema["fields"]]
    constraints = []
    # add constraints from columns
    for c in table_schema["fields"]:
        constraints += get_field_constraints(c)
    if table_schema.get("primaryKey"):
        constraints.append(get_pk(table_schema["primaryKey"]))
    for d in table_schema.get("uniqueKeys", []):
        constraints.append(get_uq(d))
    for d in table_schema.get("foreignKeys", []):
        constraints.append(get_fk(d))
    tab = Table(
        name, meta, *columns, *constraints, comment=description, schema=schema_name
    )
    return tab


def get_meta(schema_json_data, url):
    eng = create_engine(url)
    meta = MetaData(eng)
    resources = schema_json_data["resources"]
    for res in resources:
        get_tab(res, meta)

    return meta


def get_json_data(schema_json):

    base_dir = os.path.dirname(schema_json)

    def loader(rel_path):
        path = os.path.join(base_dir, rel_path)
        with open(path, encoding="utf-8") as file:
            return json.load(file)

    with open(schema_json, encoding="utf-8") as file:
        data = jsonref.load(file, loader=loader)

    return data
