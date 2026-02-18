from __future__ import annotations

from typing import TYPE_CHECKING

from textnode import TextType

if TYPE_CHECKING:
    from textnode import TextNode


class HTMLNode:
    """Base class for HTML DOM nodes.

    Attributes:
        tag: HTML element tag name (e.g. "p", "div"). None for raw text.
        value: Text content of the node.
        children: Child HTMLNode instances.
        props: HTML attributes as a dict (e.g. {"href": "..."}).
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        """Render this node to an HTML string. Must be implemented by subclasses."""
        raise NotImplementedError("to_html method must be implemented by subclasses")

    def props_to_html(self) -> str:
        """Render the node's props dict as an HTML attribute string."""
        if not self.props:
            return ""
        result = ""
        for key, value in self.props.items():
            result += f' {key}="{value}"'
        return result

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )


class LeafNode(HTMLNode):
    """An HTML node with a text value and no children.

    Args:
        tag: HTML tag name, or None for a raw text node.
        value: The text content to render.
        props: Optional HTML attributes.
    """

    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"


class ParentNode(HTMLNode):
    """An HTML node that contains child nodes.

    Args:
        tag: HTML tag name (required).
        children: Non-empty list of child HTMLNode instances.
        props: Optional HTML attributes.
    """

    def __init__(
        self,
        tag: str | None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode(tag={self.tag!r}, children={self.children!r}, props={self.props!r})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    """Convert a TextNode into the corresponding LeafNode HTML element.

    Args:
        text_node: The inline text node to convert.

    Returns:
        A LeafNode representing the text node as HTML.

    Raises:
        ValueError: If the text node's type is not recognised.
    """
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


