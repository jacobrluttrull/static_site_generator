from textnode import TextNode, TextType
from extract_links import extract_markdown_images, extract_markdown_links

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only process TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all images from this node's text
        images = extract_markdown_images(node.text)

        # If no images, keep the node as is
        if not images:
            new_nodes.append(node)
            continue

        # Split the text around each image
        remaining_text = node.text
        for alt_text, url in images:
            # Split on the full image markdown syntax
            parts = remaining_text.split(f"![{alt_text}]({url})", 1)

            # Add text before the image (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

            # Continue with remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""

        # Add any remaining text after the last image
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # Only process TEXT nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        # Extract all links from this node's text
        links = extract_markdown_links(node.text)

        # If no links, keep the node as is
        if not links:
            new_nodes.append(node)
            continue

        # Split the text around each link
        remaining_text = node.text
        for anchor_text, url in links:
            # Split on the full link markdown syntax
            parts = remaining_text.split(f"[{anchor_text}]({url})", 1)

            # Add text before the link (if any)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))

            # Continue with remaining text
            remaining_text = parts[1] if len(parts) > 1 else ""

        # Add any remaining text after the last link
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes