"""Inline markdown processing: delimiter splitting, link/image extraction, and text-to-node conversion."""

from __future__ import annotations

import re

from textnode import TextNode, TextType


# ---------------------------------------------------------------------------
# Regex-based extraction
# ---------------------------------------------------------------------------

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extract all markdown image references from *text*.

    Args:
        text: Raw markdown string.

    Returns:
        List of (alt_text, url) tuples for each ``![alt](url)`` found.
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extract all markdown link references from *text*, ignoring images.

    Args:
        text: Raw markdown string.

    Returns:
        List of (anchor_text, url) tuples for each ``[text](url)`` found.
    """
    pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


# ---------------------------------------------------------------------------
# Delimiter-based splitting
# ---------------------------------------------------------------------------

def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Split plain-text nodes on *delimiter*, tagging inner segments with *text_type*.

    Non-TEXT nodes are passed through unchanged.

    Args:
        old_nodes: Input list of TextNode instances.
        delimiter: The markdown delimiter string (e.g. ``"**"``, ``"`"``).
        text_type: The TextType to assign to delimited segments.

    Returns:
        Expanded list of TextNode instances.

    Raises:
        ValueError: If a TEXT node contains an unclosed delimiter.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(
                f"Delimiter '{delimiter}' appears an even number of times in text: '{node.text}'"
            )

        for i, part in enumerate(parts):
            if not part:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


# ---------------------------------------------------------------------------
# Image and link splitting
# ---------------------------------------------------------------------------

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Replace inline image markdown in TEXT nodes with IMAGE TextNode instances.

    Args:
        old_nodes: Input list of TextNode instances.

    Returns:
        Expanded list where ``![alt](url)`` sequences become IMAGE nodes.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt_text, url in images:
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Replace inline link markdown in TEXT nodes with LINK TextNode instances.

    Args:
        old_nodes: Input list of TextNode instances.

    Returns:
        Expanded list where ``[text](url)`` sequences become LINK nodes.
    """
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for anchor_text, url in links:
            parts = remaining_text.split(f"[{anchor_text}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            remaining_text = parts[1] if len(parts) > 1 else ""

        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


# ---------------------------------------------------------------------------
# Full inline pipeline
# ---------------------------------------------------------------------------

def text_to_textnodes(text: str) -> list[TextNode]:
    """Convert a plain text string into a list of TextNode instances.

    Applies all inline markdown transformations in order:
    bold → italic (``*``) → italic (``_``) → code → images → links.

    Args:
        text: Raw inline markdown text.

    Returns:
        List of TextNode instances representing the parsed inline content.
    """
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes