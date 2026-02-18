# Re-export shim – implementation lives in file_operations.py
from file_operations import generate_pages_recursive

__all__ = ["generate_pages_recursive"]