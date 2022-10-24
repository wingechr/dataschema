import logging  # noqa

from sqlalchemy import ForeignKeyConstraint, create_mock_engine

from .dot import Digraph, Edge, Node, Subgraph


class Compiler:
    def __init__(self, url, init_data=None):
        self.data = init_data or []
        self.engine = create_mock_engine(url, self)

    def __call__(self, table, *args, **kwargs):
        if args:
            raise NotImplementedError(args)
        if kwargs:
            raise NotImplementedError(kwargs)
        self.compile_table(table)

    def compile_table(self, create_stmt):
        raise NotImplementedError

    def compile_tables(self, meta):
        meta.create_all(self.engine)
        return self

    def __str__(self):
        raise NotImplementedError


class DDLCompiler(Compiler):
    def __init__(self, url):
        super().__init__(url=url, init_data=[])

    def compile_table(self, create_stmt):
        self.data.append(create_stmt.compile(dialect=self.engine.dialect))

    def __str__(self):
        return "\n".join(str(x) for x in self.data)


def _get_col_index(col):
    for i, c in enumerate(col.table.columns):
        if c == col:
            return i + 1
    raise ValueError(col)


class DotCompiler(Compiler):
    def __init__(self):
        self.graph = Digraph(
            graph_attrs={
                "rankdir": "RL",
                "ranksep": 3,
                # "splines": "line"
            },
            edge_attrs={
                "arrowhead": "vee",
            },
        )
        super().__init__(
            url="sqlite://",
            init_data=self.graph,
        )
        self.clusters = {}

    def get_cluster(self, name):
        name = name or "main"
        if name not in self.clusters:
            self.clusters[name] = self.graph.append(Subgraph(name))
        return self.clusters[name]

    def compile_table(self, create_stmt):
        table = create_stmt.element
        name = table.name
        cluster = self.get_cluster(table.schema)
        label = self.get_html_table_label(table)
        table_node = cluster.append(Node(name, {"label": label, "shape": "box"}))

        for const in table.constraints:
            if isinstance(const, ForeignKeyConstraint):
                ref_table = const.referred_table
                for refcol in const.elements:
                    idx1 = _get_col_index(refcol.parent)
                    idx2 = _get_col_index(refcol.column)
                    cluster.append(
                        Edge(table_node, ref_table.name, anchor1=idx1, anchor2=idx2)
                    )

    @staticmethod
    def get_html_table_label(table):
        rows = [
            f'<tr><td port="0" align="left"><b>{table.name}</b></td></tr>',
            "<hr/>",
        ]
        pk_cols = table.primary_key.columns
        for i, col in enumerate(table.columns):

            if col.nullable:
                title = f"<i>{col.name}</i>"
            else:
                title = f"<b>{col.name}</b>"
            if col.name in pk_cols:
                title = f"<u>{title}</u>"

            rows.append(
                f'<tr><td port="{i+1}" align="left">{title}: {col.type}</td></tr>'
            )
        text = '<table border="0" cellspacing="5" cellpadding="0">%s</table>' % "".join(
            rows
        )
        return text

    def __str__(self):
        return str(self.data)
