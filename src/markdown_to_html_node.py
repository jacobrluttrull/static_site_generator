from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from textnode import TextNode, TextType
from markdown_to_blocks import markdown_to_blocks
from blocktype import block_to_block_type, BlockType
from text_to_textnodes import text_to_textnodes



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        block_nodes.append(block_to_html_node(block, block_type))

    return ParentNode("div", block_nodes)

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    else:
        raise ValueError(f"Unsupported block type: {block_type}")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level+1:]  # Skip the hashes and the space
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)
def code_to_html_node(block):
    code = block[4:-3]
    code_node = LeafNode("code", code)
    return ParentNode("pre", [code_node])
def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned_lines = []
    for line in lines:
        # Remove > and optional space
        if line.startswith("> "):
            cleaned_lines.append(line[2:])
        else:
            cleaned_lines.append(line[1:])

    text = "\n".join(cleaned_lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)
def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:].lstrip()
        children = text_to_children(text)
        items.append(ParentNode("li", children))

    return ParentNode("ul", items)

def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line.split(". ", 1)[1].lstrip()
        children = text_to_children(text)
        items.append(ParentNode("li", children))
    return ParentNode("ol", items)

