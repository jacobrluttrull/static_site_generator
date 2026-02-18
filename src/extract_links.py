# Re-export shim – implementation lives in inline_markdown.py
from inline_markdown import extract_markdown_images, extract_markdown_links

__all__ = ["extract_markdown_images", "extract_markdown_links"]