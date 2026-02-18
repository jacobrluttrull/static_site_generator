# Re-export shim – implementation lives in file_operations.py
from file_operations import extract_title

__all__ = ["extract_title"]