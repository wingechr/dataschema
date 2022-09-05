import logging
import subprocess as sp
from os import remove
from shutil import which
from tempfile import mktemp

from utils.code import Code


def _get_dot() -> str:
    path = which("dot")
    if not path:
        raise FileNotFoundError("dot")
    return path


def _process(cmd: list[str], stdin: str) -> None:
    stdin = stdin.encode()
    logging.debug(" ".join(cmd))
    proc = sp.Popen(cmd, stderr=sp.PIPE, stdin=sp.PIPE)
    _out, err = proc.communicate(input=stdin)
    if proc.returncode != 0:
        err = err.decode()
        raise Exception(err)


def make_img(dot: str, img_type: str = "png") -> bytes:
    fp = mktemp()
    cmd = [
        _get_dot(),
        f"-T{img_type}",
        f"-o{fp}",
    ]
    dot = str(dot)
    logging.debug(dot)
    _process(cmd, dot)
    with open(fp, "rb") as file:
        img_bytes = file.read()
    remove(fp)
    return img_bytes


class _DotComponent(Code):

    _used_names = set()

    @staticmethod
    def _parse_attrs(attributes):
        items = []
        for k, v in attributes.items():
            v = str(v)
            if v.startswith("<"):  # html
                v = f"<{v}>"
            else:
                v = f'"{v}"'
            items.append(f"{k}={v}")
        return " ".join(items)

    def __init__(
        self, prefix=None, name=None, attributes=None, is_group=False, parts=None
    ):
        if name:
            if name in self._used_names:
                raise ValueError(f"Duplicate name: {name}")
            self._used_names.add(name)

        self.name = name

        line = [
            prefix,
            f'"{name}"' if name else None,
            "[" + self._parse_attrs(attributes) + "]" if attributes else None,
        ]

        line = " ".join(x for x in line if x is not None)

        if is_group:
            super().__init__(header=line + "{", footer="}", parts=parts)
        else:
            assert not parts
            super().__init__(parts=[line + ";"])


class _Graph(_DotComponent):
    def __init__(
        self, prefix, name, parts, graph_attrs=None, node_attrs=None, edge_attrs=None
    ):
        parts = list(parts)
        if graph_attrs:
            parts.insert(0, _DotComponent(prefix="graph", attributes=graph_attrs))
        if node_attrs:
            parts.insert(0, _DotComponent(prefix="node", attributes=node_attrs))
        if edge_attrs:
            parts.insert(0, _DotComponent(prefix="edge", attributes=edge_attrs))
        super().__init__(prefix=prefix, name=name, is_group=True, parts=parts)


class Digraph(_Graph):
    def __init__(self, *parts, graph_attrs=None, node_attrs=None, edge_attrs=None):
        super().__init__(
            prefix="digraph",
            name="main",
            parts=parts,
            graph_attrs=graph_attrs,
            node_attrs=node_attrs,
            edge_attrs=edge_attrs,
        )


class Subgraph(_Graph):
    def __init__(
        self, name, *parts, graph_attrs=None, node_attrs=None, edge_attrs=None
    ):
        name = "cluster_" + name
        super().__init__(
            prefix="subgraph",
            name=name,
            parts=parts,
            graph_attrs=graph_attrs,
            node_attrs=node_attrs,
            edge_attrs=edge_attrs,
        )


class Node(_DotComponent):
    def __init__(self, name, node_attrs=None):
        super().__init__(name=name, attributes=node_attrs)


class Edge(_DotComponent):
    def __init__(self, node1, node2, edge_attrs=None, anchor1=None, anchor2=None):
        node1 = node1.name if isinstance(node1, Node) else node1
        node2 = node2.name if isinstance(node2, Node) else node2
        anchor1 = f':"{anchor1}"' if anchor1 else ""
        anchor2 = f':"{anchor2}"' if anchor2 else ""
        prefix = f'"{node1}"{anchor1} -> "{node2}"{anchor2}'
        super().__init__(prefix=prefix, attributes=edge_attrs)
