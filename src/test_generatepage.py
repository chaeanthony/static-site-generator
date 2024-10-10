import unittest

from generatepage import extract_title, generate_page


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Hello\nText\nText"), "Hello")

    def test_extract_title_none(self):
        with self.assertRaises(Exception):
            extract_title("Hello\nText\nText")

    def test_generate_page(self):
        pass
