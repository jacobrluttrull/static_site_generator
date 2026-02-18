from __future__ import annotations

from enum import Enum


class TextType(Enum):
    """Enum representing the type of inline text formatting."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Represents an inline text segment with optional formatting and URL.

    Attributes:
        text: The raw text content.
        text_type: The formatting type (e.g. BOLD, ITALIC, LINK).
        url: Optional URL for LINK and IMAGE nodes.
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text!r}, {self.text_type}, {self.url!r})"


