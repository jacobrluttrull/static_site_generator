# Re-export shim – implementation lives in block_markdown.py
from block_markdown import markdown_to_blocks

__all__ = ["markdown_to_blocks"]