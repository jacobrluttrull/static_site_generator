import os
from generate_page import generate_page

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """
    Recursively generate HTML pages for all markdown files in a directory.

    Args:
        dir_path_content: Source directory containing markdown files
        template_path: Path to the HTML template
        dest_dir_path: Destination directory for generated HTML files
    """
    # List all items in the content directory
    items = os.listdir(dir_path_content)

    for item in items:
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            # If it's a markdown file, generate HTML
            if src_path.endswith('.md'):
                # Replace .md with .html for destination
                dest_path = dest_path.replace('.md', '.html')
                generate_page(src_path, template_path, dest_path)
        elif os.path.isdir(src_path):
            # If it's a directory, recurse into it
            generate_pages_recursive(src_path, template_path, dest_path)