import sys
from textnode import TextNode, TextType
from copy_directory import copy_directory
from generate_pages_recursive import generate_pages_recursive

def main():
    # Get basepath from command line, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    # Copy static files to docs directory
    copy_directory("static", "docs")

    # Generate all pages recursively
    generate_pages_recursive("content", "template.html", "docs", basepath)

    print("\n" + "="*50)
    print(f"Site generated successfully with basepath: {basepath}")
    print("="*50)

if __name__ == "__main__":
    main()