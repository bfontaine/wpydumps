# -*- coding: UTF-8 -*-

from collections import deque
from typing import Callable, Optional, Any, Deque, cast
from xml import sax

from wpydumps.model import Page, Revision, Contributor
from wpydumps.archive import get_reader

PageCallbackType = Callable[[Page], Any]


class PageHandler(sax.handler.ContentHandler):
    """
    SAX handler to parse page revisions from a Wikipedia dump.
    It calls ``page_callback`` on each ``wpydumps.model.Page`` it parses.

    Options:

    * ``keep_revisions_text`` (default ``True``): keep the revision text. If
      ``False``, drop it and set only `Revision.text_length`.

    Format: https://en.wikipedia.org/wiki/Help:Export.
    """

    def __init__(self, page_callback: PageCallbackType, keep_revisions_text=True):
        super().__init__()
        self.page_callback = page_callback
        self._keep_revisions_text = keep_revisions_text

        self._elements: Deque[str] = deque()
        self._current_page: Optional[Page] = None
        self._current_revision: Optional[Revision] = None
        self._current_contributor: Optional[Contributor] = None
        self._current_content: Optional[str] = None

        self._previous_revision_text_length: Optional[int] = None

    def _printState(self):
        print(list(self._elements))

    def currentElement(self):
        if self._elements:
            return self._elements[-1]

    def parentElement(self):
        if len(self._elements) >= 2:
            return self._elements[-2]

    def startElement(self, name, attrs):
        self._elements.append(name)

        if name == "page":
            self._current_page = Page()
            self._previous_revision_text_length = 0
            return

        parent = self.parentElement()
        if parent == "page":
            if name == "redirect":
                self._current_page.redirect = attrs["title"]
                return
            elif name == "revision":
                self._current_revision = Revision()
                return

        if parent == "revision":
            if name == "minor":
                self._current_revision.minor = True
                return
            elif name == "contributor":
                if "deleted" in attrs:
                    self._current_revision.deleted_contributor = True
                    return
                else:
                    self._current_contributor = Contributor()
                    return
            elif name == "text" and "deleted" in attrs:
                self._current_revision.deleted_text = True
                return

    def characters(self, content: str):
        if self._current_content is None:
            self._current_content = content
        else:
            self._current_content += content

    def endElement(self, name):
        parent = self.parentElement()
        element = self.currentElement()
        revision = self._current_revision
        self._elements.pop()

        content = self._current_content
        self._current_content = None

        if name == "page":
            self.page_callback(self._current_page)
            self._current_page = None
            return

        if name == "revision":
            revision = self._current_revision
            if revision.text_length is None:
                revision.text_length = 0

            revision.diff_length = revision.text_length - self._previous_revision_text_length
            self._previous_revision_text_length = revision.text_length

            self._current_page.revisions.append(revision)
            self._current_revision = None
            return

        if name == "contributor":
            self._current_revision.contributor = self._current_contributor
            self._current_contributor = None
            return

        # text fields

        if content is None:
            return

        original_content = content
        content = content.strip()

        if parent == "page":
            page = cast(Page, self._current_page)

            if element == "ns":
                page.namespace = content
            elif element == "id":
                page.id = content
            elif element == "restrictions":
                page.restrictions = content
            elif element == "title":
                page.title = content

            return

        if parent == "revision":
            if element == "text":
                if self._keep_revisions_text:
                    revision.text = original_content
                    revision.text_length = len(original_content)
                else:
                    revision.text_length = 0

            elif element == "timestamp":
                revision.timestamp = content
            elif element == "comment":
                revision.comment = content
            elif element == "id":
                revision.id = content
            elif element == "parentid":
                revision.parent_id = content
            elif element == "model":
                revision.model = content
            elif element == "format":
                revision.format = content
            elif element == "sha1":
                revision.sha1 = content

            return

        if parent == "contributor":
            contributor = cast(Contributor, self._current_contributor)

            if element == "id":
                contributor.id = content
            elif element == "username":
                contributor.username = content
            elif element == "ip":
                contributor.ip = content

            return


def parse_pages_from_reader(reader, page_callback: PageCallbackType,
                            keep_revisions_text=True):
    """
    Parse pages from a file-like reader. Call ``page_callback`` on each parsed
    page. See ``PageHandler`` for the keyword arguments.
    """
    handler = PageHandler(page_callback, keep_revisions_text=keep_revisions_text)
    sax.parse(reader, handler)


def parse_pages_from_archive_filename(filename: str, page_callback: PageCallbackType,
                                      keep_revisions_text=True):
    """
    Parse pages from an archive file. See ``parse_pages_from_reader``.
    """
    return parse_pages_from_reader(get_reader(filename), page_callback,
                                   keep_revisions_text=keep_revisions_text)
