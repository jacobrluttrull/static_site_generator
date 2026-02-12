import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(' '))

    def test_props_to_html_empty_props(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_special_characters(self):
        node = HTMLNode(props={"class": "btn-primary", "data-id": "123"})
        result = node.props_to_html()
        self.assertIn('class="btn-primary"', result)
        self.assertIn('data-id="123"', result)

    def test_node_with_tag_only(self):
        node = HTMLNode(tag="p")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_with_value_only(self):
        node = HTMLNode(value="Hello World")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello World")

    def test_node_with_children(self):
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].value, "Child 1")

    def test_node_all_parameters(self):
        child = HTMLNode(tag="span", value="child")
        node = HTMLNode(
            tag="div",
            value="parent",
            children=[child],
            props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "parent")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props["class"], "container")


if __name__ == "__main__":
    unittest.main()