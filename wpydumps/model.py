# -*- coding: UTF-8 -*-
from typing import Optional, Iterable


def _repr(obj, attrs_string):
    name = "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__)
    return '<%s %s>' % (name, attrs_string)


class Contributor:
    def __init__(self):
        self.id: Optional[str] = None
        self.username: Optional[str] = None
        self.ip: Optional[str] = None

    def __repr__(self):
        if self.ip:
            return _repr(self, 'ip="%s"' % self.ip)
        return _repr(self, 'id=%s "%s"' % (self.id, self.username))


class Revision:
    def __init__(self):
        self.id: Optional[str] = None
        self.parent_id: Optional[str] = None
        self.timestamp: Optional[str] = None  # e.g. "2010-12-22T15:34:44Z"
        self.contributor: Optional[Contributor] = None
        self.comment: Optional[str] = None
        self.text: Optional[str] = None
        self.text_length: Optional[int] = None
        self.diff_length: Optional[int] = None
        self.minor: Optional[bool] = False
        self.deleted_text: Optional[bool] = False
        self.deleted_contributor: Optional[bool] = False
        self.model: Optional[str] = None  # "wikitext", "javascript", "css"
        self.format: Optional[str] = None  # "text/x-wiki", "text/javascript", "text/css"
        self.sha1: Optional[str] = None

    def __repr__(self):
        return _repr(self, 'id=%s m=%s' % (self.id, self.minor))


class Page:
    def __init__(self):
        self.title: Optional[str] = None
        self.namespace: Optional[str] = None
        self.id: Optional[str] = None
        self.redirect: Optional[str] = None
        self.restrictions: Optional[str] = None
        self.revisions: Iterable[Revision] = []

    def __repr__(self):
        return _repr(self, 'title="%s"' % self.title)
