from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    def props_to_html(self):
        if not self.props:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"
class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if not self.children:
            raise ValueError("ParentNode must have children")

        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
    def __repr__(self):
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"
def text_node_to_html_node(text_node):
    conversions = {
        TextType.TEXT: lambda node: LeafNode(None, node.text),
        TextType.BOLD: lambda node: LeafNode("b", node.text),
        TextType.ITALIC: lambda node: LeafNode("i", node.text),
        TextType.CODE: lambda node: LeafNode("code", node.text),
        TextType.LINK: lambda node: LeafNode("a", node.text, {"href": node.url}),
        TextType.IMAGE: lambda node: LeafNode("img", "", {"src": node.url, "alt": node.text}),
    }

    if text_node.text_type not in conversions:
        raise ValueError(f"Unknown text type: {text_node.text_type}")

    return conversions[text_node.text_type](text_node)


