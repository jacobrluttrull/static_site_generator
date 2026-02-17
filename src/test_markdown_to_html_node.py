import unittest
from markdown_to_html_node import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# This is an h1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>This is an h1</h1></div>")
    def test_heading_multiple_levels(self):
        md = """
    # H1

    ## H2

    ### H3
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>H1</h1><h2>H2</h2><h3>H3</h3></div>",
        )

    def test_quote(self):
        md = """> This is a quote
> with multiple lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nwith multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second item
- Third item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First
2. Second
3. Third
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Heading

This is a paragraph with **bold** text.

- List item 1
- List item 2

> A quote here
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Heading</h1>", html)
        self.assertIn("<p>This is a paragraph with <b>bold</b> text.</p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>List item 1</li>", html)
        self.assertIn("<blockquote>A quote here</blockquote>", html)

    def test_list_with_inline_markdown(self):
        md = """
- Item with **bold**
- Item with `code`
- Item with *italic*
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<li>Item with <b>bold</b></li>", html)
        self.assertIn("<li>Item with <code>code</code></li>", html)
        self.assertIn("<li>Item with <i>italic</i></li>", html)

if __name__ == "__main__":
    unittest.main()