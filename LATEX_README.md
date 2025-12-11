# 📄 LaTeX SRS Document

## Overview
This directory contains a professionally formatted LaTeX version of the Software Requirements Specification (SRS) document.

## Files
- **SRS_Document.tex** - Main LaTeX source file
- **compile_latex.sh** - Compilation script
- **SRS_Document.pdf** - Generated PDF (after compilation)

## Compilation

### Prerequisites
You need a LaTeX distribution installed:
- **macOS**: `brew install --cask mactex` or `brew install basictex`
- **Linux**: `sudo apt-get install texlive-full`
- **Windows**: Install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

### Compile the Document

#### Option 1: Using the Script (Recommended)
```bash
bash compile_latex.sh
```

#### Option 2: Manual Compilation
```bash
pdflatex SRS_Document.tex
pdflatex SRS_Document.tex  # Run twice for table of contents
```

### Output
After compilation, you'll get:
- **SRS_Document.pdf** - The final PDF document

## Document Features

### Professional Formatting
- ✅ Professional title page
- ✅ Table of contents
- ✅ List of figures and tables
- ✅ Color-coded sections
- ✅ Custom info boxes
- ✅ Code listings with syntax highlighting
- ✅ Hyperlinks (clickable in PDF)

### Sections Included
1. Introduction
2. Overall Description
3. System Features
4. External Interface Requirements
5. System Architecture
6. Non-Functional Requirements
7. User Stories
8. Use Cases
9. Data Model
10. Security Requirements
11. Performance Requirements
12. Testing Requirements
13. Deployment Requirements
14. Appendices

### Packages Used
- `babel` - Multi-language support (English/Arabic)
- `geometry` - Page layout
- `hyperref` - Clickable links
- `xcolor` - Colors
- `fancyhdr` - Headers and footers
- `tcolorbox` - Colored boxes
- `listings` - Code syntax highlighting
- `booktabs` - Professional tables

## Customization

### Colors
Edit the color definitions in the preamble:
```latex
\definecolor{primaryblue}{RGB}{0,102,204}
\definecolor{secondaryblue}{RGB}{51,153,255}
\definecolor{accentorange}{RGB}{255,140,0}
```

### Document Information
Edit these variables:
```latex
\newcommand{\version}{1.0}
\newcommand{\docdate}{December 11, 2025}
```

## Troubleshooting

### Missing Packages
If you get "Package not found" errors:
```bash
# macOS (MacTeX)
tlmgr install <package-name>

# Linux
sudo apt-get install texlive-<package-name>
```

### Compilation Errors
- Run `pdflatex` twice (needed for table of contents)
- Check for missing packages
- Ensure all files are in the same directory

## Online Compilation

If you don't want to install LaTeX locally, use online services:
- [Overleaf](https://www.overleaf.com/) - Free online LaTeX editor
- [ShareLaTeX](https://www.sharelatex.com/) - Online LaTeX editor

Just upload `SRS_Document.tex` and compile online!

## Output Quality

The generated PDF will have:
- ✅ Professional appearance
- ✅ Proper page numbering
- ✅ Clickable table of contents
- ✅ Hyperlinked references
- ✅ Color-coded sections
- ✅ Print-ready format

---

**Happy Typesetting! 📝**

