# -*- coding: UTF-8 -*-

def _repr(obj, attrs_string):
    name = "%s.%s" % (obj.__class__.__module__, obj.__class__.__name__)
    return '<%s %s>' % (name, attrs_string)

class Contributor:
    def __init__(self):
        self.id = None
        self.username = None
        self.ip = None

    def __repr__(self):
        if self.ip:
            return _repr(self, 'ip="%s"' % self.ip)
        return _repr(self, 'id=%s "%s"' % (self.id, self.username))


class Revision:
    def __init__(self):
        self.id = None
        self.parent_id = None
        self.timestamp = None
        self.contributor = None
        self.comment = None
        self.text = None
        self.text_length = -1
        self.minor = False
        self.deleted_text = False
        self.deleted_contributor = False
        self.model = None
        self.format = None
        self.sha1 = None

    def __repr__(self):
        return _repr(self, 'id=%s m=%s' % (self.id, self.minor))


class Page:
    def __init__(self):
        self.title = None
        self.namespace = None
        self.id = None
        self.redirect = None
        self.restrictions = None
        self.revisions = []

    def __repr__(self):
        return _repr(self, 'title="%s"' % self.title)
