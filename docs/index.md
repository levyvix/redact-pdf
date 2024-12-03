# redact-pdf

[![Release](https://img.shields.io/github/v/release/levyvix/redact-pdf)](https://img.shields.io/github/v/release/levyvix/redact-pdf)
[![Build status](https://img.shields.io/github/actions/workflow/status/levyvix/redact-pdf/main.yml?branch=main)](https://github.com/levyvix/redact-pdf/actions/workflows/main.yml?query=branch%3Amain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/levyvix/redact-pdf)](https://img.shields.io/github/commit-activity/m/levyvix/redact-pdf)
[![License](https://img.shields.io/github/license/levyvix/redact-pdf)](https://img.shields.io/github/license/levyvix/redact-pdf)

Redact a phrase off a pdf file

---

## Installation

```bash
pip install redact-pdf
```

## Usage

Use the project in a python file

```python
from redact_pdf.redact import TextRedactor

from pathlib import Path

pdf_file = Path(__file__).parent / "pdf_test.pdf"
save_path = Path(__file__).parent / "pdf_test_redacted.pdf"

tr = TextRedactor()
tr.redact_text(
	file_path=pdf_file,
	text_to_redact="XXX",
	output_file_name=save_path,
)
```

This will result in a .pdf file called `pdf_test_redacted.pdf` with the phrase `XXX` **removed from every page**.
