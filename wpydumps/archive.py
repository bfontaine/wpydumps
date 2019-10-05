# -*- coding: UTF-8 -*-

import io
import libarchive.public

class Wp7zReader(io.RawIOBase):
    """
    File-like reader that can read 7z archives. It extract each entry of the
    archive one-by-one, with no separation between them. Wikipedia dumps always
    contain only one entry anyway.

    This is a wrapper around libarchive.public.file_reader.
    """

    def __init__(self, filename):
        self.filename = filename
        self._blocks = self._open_blocks()
        self._block = None
        self._cursor = 0

    def readable(self): return True
    def writable(self): return False
    def seekable(self): return False
    def close(self): pass

    def readinto(self, b):
        if not self._block or self._cursor == len(self._block):
            self._next_block()
            if not self._block:
                # EOF
                return 0

        size = min(len(b), len(self._block) - self._cursor)
        b[0:size] = self._block[self._cursor:self._cursor + size]
        self._cursor += size
        return size

    def _next_block(self):
        try:
            self._block = next(self._blocks)
            self._cursor = 0
        except StopIteration:
            return

    def _open_blocks(self):
        with libarchive.public.file_reader(self.filename) as entries:
            for entry in entries:
                for block in entry.get_blocks():
                    yield block
                break
