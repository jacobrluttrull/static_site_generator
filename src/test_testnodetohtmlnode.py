import unittest
from htmlnode import text_node_to_html_node
from textnode import TextNode, TextType


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_type(self):
        node = TextNode("Just plain text", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "Just plain text")

    def test_bold_type(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_type(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_type(self):
        node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_link_type(self):
        node = TextNode("Click here", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Click here</a>')

    def test_image_type(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.png" alt="Alt text"></img>')

    def test_image_type_empty_alt(self):
        node = TextNode("", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        html = html_node.to_html()
        self.assertIn('src="https://example.com/image.png"', html)
        self.assertIn('alt=""', html)

    def test_link_with_special_chars(self):
        node = TextNode("Link & Text", TextType.LINK, "https://example.com?foo=bar&baz=qux")
        html_node = text_node_to_html_node(node)
        html = html_node.to_html()
        self.assertIn('href="https://example.com?foo=bar&baz=qux"', html)
        self.assertIn('Link & Text', html)


if __name__ == "__main__":
    unittest.main()