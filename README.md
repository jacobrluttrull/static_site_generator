# Static Site Generator

A static site generator built from scratch in Python that converts Markdown content into a fully static HTML/CSS website.

## About

This project processes raw Markdown files and images to generate a complete static website. Static sites are fast, secure, and easy to host — perfect for blogs, portfolios, and documentation.

The generator features:
- Full Markdown-to-HTML conversion with support for headings, paragraphs, lists, code blocks, quotes, bold, italic, links, and images
- Recursive directory traversal to process nested content
- Template-based HTML generation
- Configurable base paths for deployment
- Automatic static asset copying

**Live Demo:** [https://jacobrluttrull.github.io/static_site_generator/](https://jacobrluttrull.github.io/static_site_generator/)

Built as a guided project through [Boot.dev](https://www.boot.dev).

## Tech Stack

- **Python 3** - Core language
- **GitHub Pages** - Hosting
- Custom recursive Markdown parser (no external libraries)

## Project Structure
```
static_site_generator/
├── content/              # Markdown source files
├── static/               # CSS, images, and other static assets
├── docs/                 # Generated HTML output (deployed to GitHub Pages)
├── src/                  # Python source code
│   ├── main.py           # Entry point
│   ├── textnode.py       # TextNode class and TextType enum
│   ├── htmlnode.py       # HTMLNode, LeafNode, ParentNode classes
│   ├── inline_markdown.py  # All inline markdown processing (links, images, delimiters)
│   ├── block_markdown.py   # All block-level markdown processing (headings, lists, etc.)
│   ├── file_operations.py  # File copying, title extraction, page generation
│   └── tests/            # Unit tests
├── template.html         # HTML template
├── build.sh              # Production build script
└── main.sh               # Local development script
```

## Getting Started

### Prerequisites

- Python 3
- Git

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/jacobrluttrull/static_site_generator.git
cd static_site_generator
```

2. Run the local development server:
```bash
./main.sh
```

This generates the site and starts a local server at `http://localhost:8888`

### Building for Production
```bash
./build.sh
```

This builds the site with the correct base path for GitHub Pages deployment.

## Deployment

The site is automatically deployed to GitHub Pages from the `/docs` directory on the `main` branch.

To deploy changes:
```bash
./build.sh
git add .
git commit -m "Update site"
git push origin main
```

GitHub Pages will automatically rebuild and deploy within 1-2 minutes.

## Features Implemented

- [x] Markdown to HTML conversion
- [x] Support for inline formatting (bold, italic, code)
- [x] Support for block elements (headings, paragraphs, lists, quotes, code blocks)
- [x] Image and link processing
- [x] Recursive page generation
- [x] Template-based HTML rendering
- [x] Static asset copying
- [x] Configurable base paths for subdirectory deployment
- [x] GitHub Pages deployment

## Testing

Run the unit tests with:
```bash
./test.sh
```

Tests live in `src/tests/` and are discovered automatically by the test runner.

## License

This project is for educational purposes as part of the Boot.dev curriculum.