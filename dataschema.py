import logging
import re

import click

from utils.compiler import DDLCompiler, DotCompiler
from utils.dot import make_img
from utils.schema import get_meta


@click.command()
@click.pass_context
@click.option(
    "--loglevel",
    "-l",
    type=click.Choice(["debug", "info", "warning", "error"]),
    default="info",
)
@click.argument("schema-json")
@click.option("--sql-dialect", "-d", default="mssql")
def main(ctx, loglevel, schema_json, sql_dialect="mssql"):
    """Script entry point."""
    if isinstance(loglevel, str):  # e.g. 'debug'/'DEBUG' -> logging.DEBUG
        loglevel = getattr(logging, loglevel.upper())
    ctx.ensure_object(dict)

    meta = get_meta(schema_json, url=f"{sql_dialect}://")

    sql = str(DDLCompiler(meta.bind.url).compile_tables(meta))
    dot = str(DotCompiler().compile_tables(meta))

    with open(re.sub(r"\.json$", ".sql", schema_json), "w", encoding="utf-8") as file:
        file.write(sql)

    with open(re.sub(r"\.json$", ".png", schema_json), "wb") as file:
        file.write(make_img(dot))


if __name__ == "__main__":
    main()
