#!/bin/bash

# Script to compile LaTeX document
# Usage: bash compile_latex.sh

echo "🔨 Compiling LaTeX document..."

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null; then
    echo "❌ Error: pdflatex is not installed"
    echo ""
    echo "Installation instructions:"
    echo "  macOS: brew install --cask mactex"
    echo "  Linux: sudo apt-get install texlive-full"
    echo "  Windows: Install MiKTeX or TeX Live"
    exit 1
fi

# Compile LaTeX document
echo "📄 Compiling SRS_Document.tex..."
pdflatex -interaction=nonstopmode SRS_Document.tex

# Run again for table of contents
echo "📑 Generating table of contents..."
pdflatex -interaction=nonstopmode SRS_Document.tex

# Clean up auxiliary files
echo "🧹 Cleaning up..."
rm -f *.aux *.log *.out *.toc *.lof *.lot

echo ""
echo "✅ Compilation complete!"
echo "📄 Output: SRS_Document.pdf"

