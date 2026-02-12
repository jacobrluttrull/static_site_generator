import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text</p>")

    def test_to_html_with_nested_parents(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold"),
                        LeafNode(None, " text"),
                    ],
                ),
            ],
        )
        self.assertEqual(node.to_html(), "<div><p><b>Bold</b> text</p></div>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello")],
            {"class": "container", "id": "main"}
        )
        html = node.to_html()
        self.assertIn('class="container"', html)
        self.assertIn('id="main"', html)
        self.assertTrue(html.startswith('<div '))
        self.assertIn('<p>Hello</p>', html)
        self.assertTrue(html.endswith('</div>'))

    def test_to_html_no_tag_raises_error(self):
        node = ParentNode(None, [LeafNode("p", "text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_children_raises_error(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_raises_error(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_multiple_children(self):
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        )

    def test_to_html_deeply_nested(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "article",
                            [
                                LeafNode("p", "Deep content"),
                            ],
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><section><article><p>Deep content</p></article></section></div>"
        )

    def test_to_html_mixed_children(self):
        node = ParentNode(
            "div",
            [
                LeafNode("h1", "Title"),
                ParentNode("p", [LeafNode("b", "Bold"), LeafNode(None, " text")]),
                LeafNode("p", "Another paragraph"),
            ],
        )
        expected = "<div><h1>Title</h1><p><b>Bold</b> text</p><p>Another paragraph</p></div>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()