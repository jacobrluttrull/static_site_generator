def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    raise Exception("No h1 header found in markdown"
                    )