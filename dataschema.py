import json
import logging
import os

import click

from utils.compiler import DDLCompiler, DotCompiler
from utils.dot import make_img
from utils.schema import get_json_data, get_meta


@click.command()
@click.pass_context
@click.option(
    "--loglevel",
    "-l",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="info",
)
@click.argument("schema-json")
@click.argument("output")
@click.option("--sql-dialect", "-d", default="mssql")
def main(ctx, loglevel, schema_json, output, sql_dialect="mssql"):
    """Script entry point."""
    if isinstance(loglevel, str):  # e.g. 'debug'/'DEBUG' -> logging.DEBUG
        loglevel = getattr(logging, loglevel.upper())
    ctx.ensure_object(dict)

    schema_json = os.path.abspath(schema_json)
    output = os.path.abspath(output)
    assert output != schema_json
    os.makedirs(os.path.dirname(output), exist_ok=True)
    suffix = output.split(".")[-1]

    json_data = get_json_data(schema_json)
    if suffix == "json":
        with open(output, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=2, ensure_ascii=False)
    elif suffix == "png":
        meta = get_meta(json_data, url=f"{sql_dialect}://")
        dot = str(DotCompiler().compile_tables(meta))
        with open(output, "wb") as file:
            file.write(make_img(dot))
    elif suffix == "sql":
        meta = get_meta(json_data, url=f"{sql_dialect}://")
        sql = str(DDLCompiler(meta.bind.url).compile_tables(meta))
        with open(output, "w", encoding="utf-8") as file:
            file.write(sql)
    else:
        raise NotImplementedError(suffix)


if __name__ == "__main__":
    main()
