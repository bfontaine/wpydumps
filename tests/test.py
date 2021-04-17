# -*- coding: UTF-8 -*-
import sys
import unittest
from os.path import dirname

if __name__ == "__main__":
    sys.path.insert(0, dirname(__file__) + "/..")

import wpydumps


class TestWPyDumps(unittest.TestCase):
    def test_version(self):
        self.assertRegexpMatches(wpydumps.__version__, r"^\d+\.\d+\.\d+")


if __name__ == "__main__":
    here = dirname(__file__)
    suite = unittest.defaultTestLoader.discover(here)
    t = unittest.TextTestRunner().run(suite)
    if not t.wasSuccessful():
        sys.exit(1)
