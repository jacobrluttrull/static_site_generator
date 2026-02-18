# Re-export shim – implementation lives in inline_markdown.py
from inline_markdown import split_nodes_image, split_nodes_link

__all__ = ["split_nodes_image", "split_nodes_link"]