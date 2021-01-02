# -*- coding: UTF-8 -*-

import io
from typing import Iterable

import libarchive.public


class UnSupportedFileTypeException(Exception):
    def __init__(self, filename: str, extensions: Iterable[str]):
        super().__init__(f"Unsupported file type: {filename}. Supported extensions: {', '.join(extensions)}.")


class Wp7zReader(io.RawIOBase):
    """
    File-like reader that can read 7z archives. It extract each entry of the
    archive one-by-one, with no separation between them. Wikipedia dumps always
    contain only one entry.

    This is a wrapper around libarchive.public.file_reader.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self._blocks = self._open_blocks()
        self._block = None
        self._cursor = 0

    def readable(self):
        return True

    def writable(self):
        return False

    def seekable(self):
        return False

    def close(self):
        pass

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return


def get_reader(filename: str):
    """
    Get a reader based on the file extension.
    """
    if filename.endswith(".7z"):
        return Wp7zReader(filename)

    # Note those are here for convenience, but using 'with open' by yourself works as well.
    if filename.endswith(".bz2"):
        import bz2
        return bz2.open(filename, "rb")

    if filename.endswith(".xml"):
        return open(filename)

    raise UnSupportedFileTypeException(filename, (".7z", ".bz2"))
