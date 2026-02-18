"""File operations: directory copying, title extraction, and HTML page generation."""

from __future__ import annotations

import os
import shutil

from block_markdown import markdown_to_html_node


# ---------------------------------------------------------------------------
# Title extraction
# ---------------------------------------------------------------------------

def extract_title(markdown: str) -> str:
    """Return the text of the first h1 heading in *markdown*.

    Args:
        markdown: Full markdown document string.

    Returns:
        The title text, stripped of surrounding whitespace.

    Raises:
        Exception: If no h1 heading (``# Title``) is found.
    """
    for line in markdown.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    raise Exception("No h1 header found in markdown")


# ---------------------------------------------------------------------------
# Directory copying
# ---------------------------------------------------------------------------

def copy_directory(src: str, dst: str) -> None:
    """Recursively copy *src* directory to *dst*, replacing *dst* if it exists.

    Args:
        src: Path to the source directory.
        dst: Path to the destination directory (will be recreated from scratch).
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    _copy_contents(src, dst)


def _copy_contents(src: str, dst: str) -> None:
    """Recursively copy the contents of *src* into *dst*."""
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        elif os.path.isdir(src_path):
            print(f"Creating directory: {dst_path}")
            os.mkdir(dst_path)
            _copy_contents(src_path, dst_path)


# ---------------------------------------------------------------------------
# Page generation
# ---------------------------------------------------------------------------

def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str = "/"
) -> None:
    """Convert a single markdown file to HTML using a template.

    Reads the markdown from *from_path* and the HTML template from
    *template_path*, converts the markdown, substitutes ``{{ Title }}`` and
    ``{{ Content }}`` placeholders, adjusts absolute paths for *basepath*,
    then writes the result to *dest_path*.

    Args:
        from_path: Path to the source ``.md`` file.
        template_path: Path to the HTML template file.
        dest_path: Destination path for the generated HTML file.
        basepath: URL base path prefix for ``href="/..."`` and ``src="/..."``
            attributes (default ``"/"``).
    """
    print(f"Generating page from {from_path} using template {template_path} to {dest_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)
    final_html = final_html.replace('href="/', f'href="{basepath}')
    final_html = final_html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content: str,
    template_path: str,
    dest_dir_path: str,
    basepath: str = "/",
) -> None:
    """Recursively convert all markdown files under *dir_path_content* to HTML.

    Mirrors the directory structure of *dir_path_content* inside *dest_dir_path*,
    converting each ``.md`` file to a corresponding ``.html`` file.

    Args:
        dir_path_content: Root directory of markdown source files.
        template_path: Path to the HTML template file.
        dest_dir_path: Root directory for generated HTML output.
        basepath: URL base path prefix forwarded to :func:`generate_page`.
    """
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(src_path):
            if src_path.endswith(".md"):
                dest_path = dest_path.replace(".md", ".html")
                generate_page(src_path, template_path, dest_path, basepath)
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path, basepath)
