from __future__ import annotations


class node:
    def __init__(self, senior):
        if type(self).__name__ == "node":
            from hebill_html_document import error
            raise error(f"Class '{self.__class__.__name__}' must be inherited.")
        self.id = id(self)
        from hebill_html_document import document
        self.document: document
        self.senior: group | None = None
        if isinstance(senior, document):
            self.document = senior
        elif isinstance(senior, group):
            self.senior = senior
            self.document = senior.document
            self.senior.juniors[self.id] = self
        else:
            from hebill_html_document import error
            raise error(f"Class '{self.__class__.__name__}' must be inherited.")
        self.document.elements[self.id] = self
        self.output_breakable = False

    def level(self) -> int:
        if self.senior is None:
            return 0
        if isinstance(self, group) and not isinstance(self, tag):
            return self.senior.level()
        return self.senior.level() + 1

    def output(self) -> str:
        pass


class code(node):
    def __init__(self, senior, text: str = None):
        super().__init__(senior)
        self.text: str = "" if text is None else text

    def output(self):
        self.document.output_next_breakable = False
        return f"{self.text}"


class comment(node):
    def __init__(self, senior, text: str = None):
        super().__init__(senior)
        self.text: str = "" if text is None else text

    def output(self):
        import html
        s = ""
        if self.document.output_break:
            s += "\n" + self.document.output_retraction * self.level()
        s += f"<!--[{html.escape(self.text)}]-->"
        self.document.output_next_breakable = True
        return s


class content(node):
    def __init__(self, senior, text: str = None):
        super().__init__(senior)
        self.text: str = "" if text is None else text

    def output(self):
        import html
        s = html.escape(self.text)
        self.document.output_next_breakable = False
        return s


class group(node):
    def __init__(self, senior):
        super().__init__(senior)
        self.juniors: dict = {}
        self._create: group_create_function_object | None = None

    def create(self):
        if self._create is None:
            self._create = group_create_function_object(self)
        return self._create

    def output(self):
        s = ""
        if len(self.juniors) > 0:
            for key, value in self.juniors.items():
                if isinstance(value, node):
                    s += value.output()
        return s


class group_create_function_object:
    def __init__(self, senior):
        self.senior = senior
        self._node: group_create_node_function_object | None = None
        self._tag: group_create_tag_function_object | None = None

    def node(self) -> group_create_node_function_object:
        if self._node is None:
            self._node = group_create_node_function_object(self.senior)
        return self._node

    def tag(self) -> group_create_tag_function_object:
        if self._tag is None:
            self._tag = group_create_tag_function_object(self.senior)
        return self._tag


class group_create_node_function_object:
    def __init__(self, senior):
        self.senior = senior

    def code(self, text: str = None):
        return code(self.senior, text)

    def content(self, text: str = None):
        return content(self.senior, text)

    def comment(self, text: str = None):
        return comment(self.senior, text)

    def group(self):
        return group(self.senior)

    def tag(self, name: str):
        return tag(self.senior, name)


class group_create_tag_function_object:
    def __init__(self, senior):
        self.senior = senior

    def a(self, title: str = None, url: str = None):
        from hebill_html_document.tags import a
        return a(self.senior, title, url)

    def body(self):
        from hebill_html_document.tags import body
        return body(self.senior)

    def div(self, text: str = None):
        from hebill_html_document.tags import div
        return div(self.senior, text)

    def head(self):
        from hebill_html_document.tags import head
        return head(self.senior)

    def html(self, lang: str = None):
        from hebill_html_document.tags import html
        return html(self.senior, lang)

    def input_text(self, name: str = None, value: str | int | float = None, placeholder: str = None):
        from hebill_html_document.tags import input_text
        return input_text(self.senior, name, value, placeholder)

    def link(self, url: str = None):
        from hebill_html_document.tags import link
        return link(self.senior, url)

    def span(self, text: str = None):
        from hebill_html_document.tags import span
        return span(self.senior, text)

    def title(self, text: str = None):
        from hebill_html_document.tags import title
        return title(self.senior, text)


class tag(group):
    def __init__(self, senior, name: str = None):
        super().__init__(senior)
        if name is not None:
            self.name = name
        else:
            n = self.__class__.__name__
            if n[-1] == "_":
                n = n[:-1]
            n.replace("_", "_")
            self.name = n
        self.attributes: dict = {}
        self.output_breakable = True

    def output(self):
        s = ""
        if self.document.output_break:
            if self.output_breakable and self.document.output_next_breakable:
                if self.level() > 0:
                    s += "\n"
            s += self.document.output_retraction * self.level()
        s += "<" + self.name
        # s += self.Attributes().output()
        if len(self.attributes) > 0:
            for n, v in self.attributes.items():
                s += f" {n}=\"{v}\""
        s += ">"
        self.document.output_next_breakable = True
        si = super().output()
        s += si
        if self.document.output_break:
            if si != "" and self.document.output_next_breakable:
                s += "\n" + "	" * self.level()
        s += "</" + self.name + ">"
        self.document.output_next_breakable = True
        return s
