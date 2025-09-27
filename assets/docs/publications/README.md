# Publications Directory

This directory contains publication-related documents and assets.

## Scripts and Generation

This directory contains:
- `genPubHTML.sh` - Shell script to generate publication HTML files from BibTeX
- `genWordCloud.py` - Python script to generate word clouds from publication abstracts
- `my-publications.bib` - BibTeX file with all publications
- Generated HTML files and word cloud images

## Usage

To generate publication files:

```bash
cd assets/docs/publications
./genPubHTML.sh [mask_name]
```

The script will:
1. Generate HTML files from BibTeX using `bibtex2html`
2. Create a word cloud from publication abstracts
3. Optionally use mask images (vader, yoda, etc.) for shaped word clouds

**Note:** The Python script is blocked from web access for security but remains functional for local generation.
