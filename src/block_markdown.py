"""Block-level markdown processing: block splitting, type detection, and HTML conversion."""

from __future__ import annotations

from enum import Enum

from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


# ---------------------------------------------------------------------------
# Block type enum
# ---------------------------------------------------------------------------

class BlockType(Enum):
    """Enum representing the structural type of a markdown block."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# ---------------------------------------------------------------------------
# Block splitting
# ---------------------------------------------------------------------------

def markdown_to_blocks(markdown: str) -> list[str]:
    """Split a markdown document into its top-level blocks.

    Blocks are separated by blank lines (``\n\n``). Leading/trailing
    whitespace is stripped from each block and empty blocks are discarded.

    Args:
        markdown: Full markdown document string.

    Returns:
        Ordered list of non-empty block strings.
    """
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


# ---------------------------------------------------------------------------
# Block type classification
# ---------------------------------------------------------------------------

def block_to_block_type(block: str) -> BlockType:
    """Classify a markdown block into its structural type.

    Args:
        block: A single stripped markdown block.

    Returns:
        The matching BlockType for the block.
    """
    # Heading: 1-6 leading '#' characters followed by a space
    if block.startswith("#"):
        count = 0
        for char in block:
            if char == "#":
                count += 1
            else:
                break
        if 1 <= count <= 6 and len(block) > count and block[count] == " ":
            return BlockType.HEADING

    # Fenced code block
    if block.startswith("```") and block.endswith("```") and len(block) > 6:
        return BlockType.CODE

    lines = block.split("\n")

    # Blockquote: every line starts with '>'
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with '- '
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: lines start with sequential '1. ', '2. ', …
    is_ordered = all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1))
    if is_ordered:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


# ---------------------------------------------------------------------------
# HTML conversion
# ---------------------------------------------------------------------------

def markdown_to_html_node(markdown: str) -> ParentNode:
    """Convert a full markdown document to an HTML node tree.

    Args:
        markdown: Full markdown document string.

    Returns:
        A ``<div>`` ParentNode containing one child node per block.
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes = [_block_to_html_node(block, block_to_block_type(block)) for block in blocks]
    return ParentNode("div", block_nodes)


def _block_to_html_node(block: str, block_type: BlockType) -> ParentNode:
    """Route a block to the appropriate HTML conversion function."""
    handlers = {
        BlockType.PARAGRAPH: _paragraph_to_html_node,
        BlockType.HEADING: _heading_to_html_node,
        BlockType.CODE: _code_to_html_node,
        BlockType.QUOTE: _quote_to_html_node,
        BlockType.UNORDERED_LIST: _unordered_list_to_html_node,
        BlockType.ORDERED_LIST: _ordered_list_to_html_node,
    }
    if block_type not in handlers:
        raise ValueError(f"Unsupported block type: {block_type}")
    return handlers[block_type](block)


def _text_to_children(text: str) -> list:
    """Convert inline markdown text to a list of HTML leaf nodes."""
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def _paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", _text_to_children(text))


def _heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", _text_to_children(text))


def _code_to_html_node(block: str) -> ParentNode:
    code = block[4:-3]
    return ParentNode("pre", [LeafNode("code", code)])


def _quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    cleaned = [line[2:] if line.startswith("> ") else line[1:] for line in lines]
    return ParentNode("blockquote", _text_to_children("\n".join(cleaned)))


def _unordered_list_to_html_node(block: str) -> ParentNode:
    items = [
        ParentNode("li", _text_to_children(line[2:].lstrip()))
        for line in block.split("\n")
    ]
    return ParentNode("ul", items)


def _ordered_list_to_html_node(block: str) -> ParentNode:
    items = [
        ParentNode("li", _text_to_children(line.split(". ", 1)[1].lstrip()))
        for line in block.split("\n")
    ]
    return ParentNode("ol", items)
