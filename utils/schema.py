import json
import logging  # noqa
import re

import jsonref
from sqlalchemy import (
    Column,
    ForeignKeyConstraint,
    MetaData,
    PrimaryKeyConstraint,
    Table,
    UniqueConstraint,
    types,
)


def parse_type(type_str):
    type_str = type_str.upper().replace(" ", "")
    m = re.match(r"^([A-Z0-9]+)(|\(.*\))$", type_str)
    name, args = m.groups()
    args = [int(x) for x in args.replace("(", "").replace(")", "").split(",") if x]
    cls = getattr(types, name)
    inst = cls(*args)
    return inst


def pop_opt(data, name, default=None):
    return data.pop(name) if name in data else default


def get_column(data):
    data = data.copy()
    name = data.pop("name")
    description = pop_opt(data, "description")
    coltype = parse_type(data.pop("type"))
    col = Column(name, coltype, comment=description, **data)
    return col


def get_pk(data):
    data = data.copy()
    name = pop_opt(data, "name")
    fields = data.pop("fields")
    return PrimaryKeyConstraint(*fields, name=name, **data)


def get_uq(data):
    data = data.copy()
    name = pop_opt(data, "name")
    fields = data.pop("fields")
    return UniqueConstraint(*fields, name=name)


def get_fk(data, meta):
    data = data.copy()
    name = pop_opt(data, "name")
    fields = data.pop("fields")
    reference = data.pop("reference")
    ref_tab = meta.tables[reference["resource"]]
    refcolumns = [ref_tab.c[c] for c in reference["fields"]]
    return ForeignKeyConstraint(fields, refcolumns=refcolumns, name=name, **data)


def get_tab(data, meta):
    data = data.copy()
    name = data.pop("name")
    description = pop_opt(data, "description")
    table_schema = data.pop("schema")
    columns = [get_column(c) for c in table_schema["fields"]]
    constraints = []
    if "primaryKey" in table_schema:
        constraints.append(get_pk(table_schema["primaryKey"]))
    for d in table_schema.get("uniqueKeys", []):
        constraints.append(get_uq(d))
    for d in table_schema.get("foreignKeys", []):
        constraints.append(get_fk(d, meta))
    tab = Table(name, meta, *columns, *constraints, comment=description, **data)
    return tab


def get_meta(table_data):
    meta = MetaData()
    with open(table_data, encoding="utf-8") as file:
        data = jsonref.load(file)
    resources = data["resources"]
    for res in resources:
        get_tab(res, meta)

    return meta
