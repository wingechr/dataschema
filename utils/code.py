class Code:
    def __init__(self, parts=None, header=None, footer=None):
        self.parts = []
        for p in parts or []:
            self.append(p)
        self.header = Code(parts=[header]) if header else None
        self.footer = Code(parts=[footer]) if footer else None
        if self.footer and not self.header:
            raise ValueError("footer without header")

    def get_lines(self, indent=0):
        if self.header:  # main body will be indented on level
            indent += 1
        indent_str = " " * (indent * 2)

        if self.header:
            yield from self.header.get_lines(indent - 1)
        for p in self.parts:
            if isinstance(p, Code):
                yield from p.get_lines(indent)
            else:
                yield indent_str + str(p)
        if self.footer:
            yield from self.footer.get_lines(indent - 1)

    def append(self, part):
        self.parts.append(part)
        return part

    def __str__(self):
        return "\n".join(self.get_lines())
