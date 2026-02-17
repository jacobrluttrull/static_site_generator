from generate_pages_recursive import generate_pages_recursive
from textnode import TextNode, TextType
from copy_directory import copy_directory

def main():
    # Copy static files to public directory
    copy_directory("static", "public")

    # Generate the HTML page
    generate_pages_recursive("content", "template.html", "public")

    print("\n" + "="*50)
    print("Testing TextNode:")
    print("="*50 + "\n")

    node1 = TextNode("This is a text node", TextType.TEXT)
    node2 = TextNode("This is bold text", TextType.BOLD)
    node3 = TextNode("Click here", TextType.LINK, "https://example.com")

    print(node1)
    print(node2)
    print(node3)

    # Test equality
    node4 = TextNode("This is a text node", TextType.TEXT)
    print(f"\nnode1 == node4: {node1 == node4}")
    print(f"node1 == node2: {node1 == node2}")

if __name__ == "__main__":
    main()