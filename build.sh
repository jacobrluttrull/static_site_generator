#!/bin/bash

# Generate the static site with default basepath
python3 src/main.py

# Navigate to docs directory and start server
cd docs
python3 -m http.server 8888