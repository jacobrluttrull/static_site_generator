import unittest
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes  # or wherever you put it

class TestTextToTextNodes(unittest.TestCase):
    def test_text_with_all_syntax(self):
        text = "This is **bold** and *italic* with `code` and ![image](https://example.com/img.png) and [link](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(nodes, expected)

    def test_plain_text_only(self):
        text = "Just plain text with no markdown"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_bold_only(self):
        text = "This has **bold text** in it"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_multiple_bold(self):
        text = "**First** and **second** bold"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("First", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.BOLD),
            TextNode(" bold", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_italic_and_bold(self):
        text = "**bold** and *italic*"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertListEqual(nodes, expected)

    def test_code_block(self):
        text = "Use `print()` to output"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Use ", TextType.TEXT),
            TextNode("print()", TextType.CODE),
            TextNode(" to output", TextType.TEXT),
        ]
        self.assertListEqual(nodes, expected)

    def test_image_only(self):
        text = "![alt text](https://example.com/image.png)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertListEqual(nodes, expected)

    def test_link_only(self):
        text = "[click here](https://example.com)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("click here", TextType.LINK, "https://example.com"),
        ]
        self.assertListEqual(nodes, expected)

    def test_multiple_images_and_links(self):
        text = "![img1](url1) and [link1](url2) then ![img2](url3)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url2"),
            TextNode(" then ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url3"),
        ]
        self.assertListEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()