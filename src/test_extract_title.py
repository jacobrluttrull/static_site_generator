import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "#  Hello World  "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_with_content(self):
        md = """
# My Title

This is some content below.
"""
        self.assertEqual(extract_title(md), "My Title")

    def test_extract_title_ignores_h2(self):
        md = """
## Not This

# This is the title

## Also not this
"""
        self.assertEqual(extract_title(md), "This is the title")

    def test_no_title_raises_exception(self):
        md = "## Just an h2\n\nNo h1 here"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_markdown_raises_exception(self):
        md = ""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()