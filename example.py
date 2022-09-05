import logging

from utils.compiler import DDLCompiler, DotCompiler
from utils.dot import make_img
from utils.schema import get_meta


def main():

    url = "mssql://"
    table_data = "example.json"

    meta = get_meta(table_data, url)

    sql = str(DDLCompiler(url).compile_tables(meta))
    dot = str(DotCompiler().compile_tables(meta))

    with open("example/example.sql", "w", encoding="utf-8") as file:
        file.write(sql)

    with open("example/example.dot", "w", encoding="utf-8") as file:
        file.write(dot)

    with open("example/example.png", "wb") as file:
        file.write(make_img(dot))


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(asctime)s %(levelname)7s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )
    main()
