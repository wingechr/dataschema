import logging

from utils.compiler import DDLCompiler, DotCompiler
from utils.dot import make_img
from utils.schema import get_meta

__version__ = "0.0.0"


def main():

    dialect = "mssql"
    table_data = "example.json"

    meta = get_meta(table_data)

    sql = str(DDLCompiler(dialect).compile_tables(meta))
    dot = str(DotCompiler().compile_tables(meta))

    with open("example.sql", "w", encoding="utf-8") as file:
        file.write(sql)

    with open("example.dot", "w", encoding="utf-8") as file:
        file.write(dot)

    with open("example.png", "wb") as file:
        file.write(make_img(dot))


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s %(levelname)7s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    main()
