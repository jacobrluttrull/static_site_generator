# Re-export shim – implementation lives in block_markdown.py
from block_markdown import BlockType, block_to_block_type

__all__ = ["BlockType", "block_to_block_type"]


