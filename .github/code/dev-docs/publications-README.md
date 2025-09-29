# Publications Directory

This directory contains publication-related documents and assets.

## Scripts and Generation

**Security Note:** Generation scripts are now stored in `.github/code/` for security and are not web-accessible.

This directory contains:

- `generate.sh` - Wrapper script to run secure publication generation
- `my-publications.bib` - BibTeX file with all publications  
- Generated HTML files and word cloud images
- Mask images (vader.png, yoda.png, etc.) for shaped word clouds

## Usage

To generate publication files:

```bash
# From publications directory (recommended)
cd assets/docs/publications
./generate.sh [mask_name]

# Or run directly (advanced)
bash .github/code/genPubHTML.sh [mask_name]
```

The generation process will:

1. Generate HTML files from BibTeX using `bibtex2html`
2. Create a word cloud from publication abstracts
3. Optionally use mask images (vader, yoda, etc.) for shaped word clouds
4. Place all output files in this directory

**Security Features:**

- Scripts are stored in `.github/code/` (web-blocked)
- Generated content remains in this directory
- Wrapper script provides convenient access
