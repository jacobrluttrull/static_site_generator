import unittest
from textnode import TextNode, TextType
from split_images_and_links import split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_images_single(self):
        node = TextNode("![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://example.com/img.png")],
            new_nodes,
        )

    def test_split_links_no_links(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_preserves_non_text_nodes(self):
        nodes = [
            TextNode("text before", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("text with ![img](url)", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        # The BOLD node should pass through unchanged
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()