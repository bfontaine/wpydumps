# -*- coding: UTF-8 -*-

import unittest
import os.path
from typing import List

from wpydumps import parser
from wpydumps.model import Page

SAMPLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sample.xml")


class TestParser(unittest.TestCase):
    def test_parse(self):
        pages: List[Page] = []

        def callback(page):
            pages.append(page)

        with open(SAMPLE_PATH) as f:
            parser.parse_pages_from_reader(f, callback, keep_revisions_text=True)

        self.assertEqual(2, len(pages))
        page1: Page = pages[0]
        page2: Page = pages[1]

        self.assertEqual("Utilisateur:Allinde/Mise en forme", page1.title)
        self.assertEqual(4, len(page1.revisions))

        self.assertEqual("ANGOA", page2.title)
        self.assertEqual("Association des producteurs de cinéma", page2.redirect)
