import os
import shutil

def copy_directory(src, dst):
    """Copy the contents of the src directory to the dst directory."""
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    _copy_contents(src, dst)
def _copy_contents(src, dst):
    """
    Helper function to recursively copy directory contents.
    """
    # List everything in the source directory
    items = os.listdir(src)

    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            # It's a file - copy it
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):  # ✅ Explicitly check if it's a directory
            # It's a directory - recurse into it
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_contents(src_path, dst_path)



