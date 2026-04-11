---
name: skill-06-doc-transform
description: >
  Convert documents between formats (PDF, DOCX, MD, LaTeX, HTML) using pandoc.
  Parse PDFs, extract text, convert papers. NEVER manually transcribe document
  content — always use this skill.
  Triggers: "convert PDF", "extract text", "DOCX to markdown", "pandoc",
  "parse document", "read PDF", "convert to LaTeX".
token_savings: 5/5
dependencies: pandoc, pdfminer.six, python-docx
---

## Install

```bash
sudo apt-get install pandoc -y
pip install pdfminer.six python-docx --break-system-packages
```

## Pandoc conversions

```bash
# MD → PDF (requires LaTeX)
pandoc paper.md -o paper.pdf --pdf-engine=xelatex

# MD → DOCX
pandoc paper.md -o paper.docx

# PDF → text (for analysis)
python3 -c "
from pdfminer.high_level import extract_text
text = extract_text('paper.pdf')
print(text[:2000])
"

# DOCX → markdown
pandoc paper.docx -t markdown -o paper.md

# LaTeX → PDF
pdflatex paper.tex
```

## For OpenCLAW paper pipeline

```bash
# Full pipeline: markdown → peer-review-ready PDF
pandoc openclaw_paper.md \
  --bibliography=refs.bib \
  --csl=ieee.csl \
  -o openclaw_paper.pdf \
  --pdf-engine=xelatex
```
