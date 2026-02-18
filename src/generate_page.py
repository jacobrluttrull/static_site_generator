# Re-export shim – implementation lives in file_operations.py
from file_operations import generate_page

__all__ = ["generate_page"]