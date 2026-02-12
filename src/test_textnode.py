import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        node2 = TextNode("Click here", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("World", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Hello", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("Text", TextType.TEXT, "https://example.com")
        node2 = TextNode("Text", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_both_url_none(self):
        node = TextNode("Plain text", TextType.TEXT, None)
        node2 = TextNode("Plain text", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_not_eq_different_text_same_url(self):
        node = TextNode("Link one", TextType.LINK, "https://example.com")
        node2 = TextNode("Link two", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_all_different(self):
        node = TextNode("Text", TextType.BOLD, "https://example.com")
        node2 = TextNode("Different", TextType.ITALIC, "https://different.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Hello", TextType.BOLD, "https://example.com")
        self.assertEqual(repr(node), "TextNode('Hello', TextType.BOLD, 'https://example.com')")

    def test_repr_no_url(self):
        node = TextNode("Hello", TextType.TEXT)
        self.assertEqual(repr(node), "TextNode('Hello', TextType.TEXT, None)")


if __name__ == "__main__":
    unittest.main()