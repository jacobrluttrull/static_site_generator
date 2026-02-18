# Re-export shim – implementation lives in file_operations.py
from file_operations import copy_directory

__all__ = ["copy_directory"]



