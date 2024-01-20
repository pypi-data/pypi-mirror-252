from __future__ import annotations
from hebill_html_document.nodes import tag, content, group


class a(tag):
    output_break_inner = False

    def __init__(self, senior, text: str = None, url: str = None):
        super().__init__(senior)
        if text is not None:
            self.create().node().content(text)
        self.attributes["href"] = ""
        if url is not None:
            self.attributes["href"] = url


class body(tag):
    def __init__(self, senior):
        super().__init__(senior)


class div(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, None)
        self.output_break_inner = False
        if text is not None:
            self.create().node().content(text)


class head(tag):
    def __init__(self, senior):
        super().__init__(senior)
        self._junior_group_for_metas: group = self.create().node().group()
        self._junior_group_for_libraries: group = self.create().node().group()
        self._junior_tag_title: title | None = None

    @property
    def junior_tag_title(self):
        if self._junior_tag_title is None:
            self._junior_tag_title = self.create().tag().title()
        return self._junior_tag_title


class html(tag):
    def __init__(self, senior, lang: str = None):
        super().__init__(senior)
        if lang is not None:
            self.attributes["lang"] = lang
        self._junior_group_for_head = self.create().node().group()
        self._junior_tag_head: head | None = None
        self._junior_tag_body: body | None = None

    @property
    def junior_tag_head(self):
        if self._junior_tag_head is None:
            self._junior_tag_head = self._junior_group_for_head.create().tag().head()
        return self._junior_tag_head

    @property
    def junior_tag_body(self):
        if self._junior_tag_body is None:
            self._junior_tag_body = self.create().tag().body()
        return self._junior_tag_body


class input_text(tag):
    def __init__(self, senior, name: str = None, value: str | int | float = None, placeholder: str = None):
        super().__init__(senior, "input")
        self.output_break_inner = False
        self.value: str | int | float = "" if value is None else value
        if name is not None:
            self.attributes["name"] = name
        if placeholder is not None:
            self.attributes["placeholder"] = placeholder


class link(tag):
    def __init__(self, senior, url: str = None):
        super().__init__(senior)
        if url is not None:
            self.attributes["href"] = url


class span(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, None)
        self.output_break_inner = False
        if text is not None:
            self.create().node().content(text)


class title(tag):
    def __init__(self, senior, text: str = None):
        super().__init__(senior, None)
        self.output_break_inner = False
        self.junior_content: content = self.create().node().content()
        if text is not None:
            self.junior_content.text = text
