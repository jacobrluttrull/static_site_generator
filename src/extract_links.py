import re

def extract_markdown_images(text):
    # Regular expression to match markdown image syntax ![alt text](image_url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    # Regular expression to match markdown link syntax [link text](url) but not images
    pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches