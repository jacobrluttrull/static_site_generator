import sys

from file_operations import copy_directory, generate_pages_recursive


def main() -> None:
    """Entry point: copy static assets and generate all HTML pages."""
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

    print("\n" + "=" * 50)
    print(f"Site generated successfully with basepath: {basepath}")
    print("=" * 50)


if __name__ == "__main__":
    main()