---
name: skill-11-latex-renderer
description: >
  Generate and compile scientific documents to PDF, HTML, LaTeX, DOCX using pandoc.
  Verified PDF engine: weasyprint. For arXiv submissions and formal papers.
  Triggers: "LaTeX", "compile PDF", "arXiv submission", "paper format",
  "render equation", "BibTeX", "scientific document", "generate PDF".
token_savings: ★★★☆☆
verified: true
dependencies: pandoc (system), weasyprint (pip)
---

## Install

```bash
# pandoc: usually pre-installed
which pandoc || sudo apt-get install pandoc -y

# PDF engine (verified working in container):
pip install weasyprint --break-system-packages

# pdflatex also available if texlive installed:
sudo apt-get install texlive-latex-base texlive-science -y
```

## Verified conversions

```bash
# MD → PDF (weasyprint — verified ✓)
pandoc paper.md -o paper.pdf --pdf-engine=weasyprint

# MD → DOCX (verified ✓)
pandoc paper.md -o paper.docx

# MD → HTML + MathJax (verified ✓)
pandoc paper.md -o paper.html --standalone --mathjax

# MD → LaTeX source (verified ✓)
pandoc paper.md -o paper.tex --standalone

# MD → PDF with metadata (verified ✓)
echo "---
title: 'My Paper'
author: 'Francisco Angulo de Lafuente'
date: '2026-04-08'
---" | cat - body.md | pandoc -o paper.pdf --pdf-engine=weasyprint
```

## arXiv-ready markdown template

```markdown
---
title: "OpenCLAW-P2P: Autonomous Peer Review"
author: "Francisco Angulo de Lafuente (ORCID: 0009-0001-1634-7063)"
date: "2026-04-08"
---

# Abstract
...

## 1. Introduction
...

## References
[1] Author, *Title*, arXiv:XXXX.XXXXX (year).
```
