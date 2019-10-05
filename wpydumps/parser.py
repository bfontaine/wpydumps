# -*- coding: UTF-8 -*-

from collections import deque
from xml import sax

from wpydumps.model import Page, Revision, Contributor
from wpydumps.archive import Wp7zReader


class PageHandler(sax.handler.ContentHandler):
    """
    SAX handler to parse page revisions from a Wikipedia dump.
    It calls ``page_callback`` on each ``wpydumps.model.Page`` it parses.

    Options:

    * ``keep_revisions_text`` (default ``False``): keep the revision text. If
      ``False``, drop it and set only `Revision.text_length`.

    Format: https://en.wikipedia.org/wiki/Help:Export.
    """

    def __init__(self, page_callback, keep_revisions_text=False):
        self.page_callback = page_callback
        self._keep_revisions_text = keep_revisions_text

        self._elements = deque()
        self._current_page = None
        self._current_revision = None
        self._current_contributor = None

        self._previous_revision_text_length = None

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
            elif name == "revision":
                self._current_revision = Revision()

        elif parent == "revision":
            if name == "minor":
                self._current_revision.minor = True
            elif name == "contributor":
                if "deleted" in attrs:
                    self._current_revision.deleted_contributor = True
                else:
                    self._current_contributor = Contributor()
            elif name == "text" and "deleted" in attrs:
                self._current_revision.deleted_text = True


    def characters(self, content):
        if content.isspace():
            return

        parent = self.parentElement()
        element = self.currentElement()

        if parent == "page":
            page = self._current_page

            if element == "ns":
                page.namespace = content
            elif element == "id":
                page.id = content
            elif element == "restrictions":
                page.restrictions = content
            elif element == "title":
                page.title = content

        elif parent == "revision":
            revision = self._current_revision

            if element == "timestamp":
                revision.timestamp = content
            elif element == "comment":
                if revision.comment is None:
                    revision.comment = ""
                revision.comment += content
            elif element == "text":
                if self._keep_revisions_text:
                    if revision.text is None:
                        revision.text = ""
                    revision.text += content

                if revision.text_length is None:
                    revision.text_length = 0

                revision.text_length += len(content)

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

        elif parent == "contributor":
            contributor = self._current_contributor

            if element == "id":
                contributor.id = content
            elif element == "username":
                contributor.username = content
            elif element == "ip":
                contributor.ip = content

    def endElement(self, name):
        self._elements.pop()

        if name == "page":
            self.page_callback(self._current_page)
            self._current_page = None

        elif name == "revision":
            revision = self._current_revision
            if revision.text_length is None:
                revision.text_length = 0

            revision.diff_length = revision.text_length - \
                self._previous_revision_text_length
            self._previous_revision_text_length = revision.text_length

            self._current_page.revisions.append(revision)
            self._current_revision = None

        elif name == "contributor":
            self._current_revision.contributor = self._current_contributor
            self._current_contributor = None

        elif self.currentElement() == "revision":
            revision = self._current_revision


def parse_pages_from_reader(reader, page_callback, **kwargs):
    """
    Parse pages from a file-like reader. Call ``page_callback`` on each parsed
    page. See ``PageHandler`` for the keyword arguments.
    """
    handler = PageHandler(page_callback, **kwargs)
    sax.parse(reader, handler)

def parse_pages_from_archive_filename(filename, page_callback, **kwargs):
    """
    Parse pages from a .7z archive file. See ``parse_pages_from_reader``.
    """
    return parse_pages_from_reader(Wp7zReader(filename), page_callback,
            **kwargs)
