import os
from pathlib import Path

import fitz  # pymupdf
from dotenv import load_dotenv


class TextRedactor:
    """Redact a text from a pdf file"""

    def redact_text(self, file_path: Path, text_to_redact: str, output_file_name: str):
        """Open the document and redact the text"""
        doc = fitz.open(file_path)
        for i in range(doc.page_count):
            page = doc.load_page(i)
            rl = page.search_for(text_to_redact, quads=True)

            if rl:  # Ensure results were found before proceeding
                page.add_redact_annot(rl[0])  # Add redaction annotation for the first match
                page.apply_redactions()  # Apply redactions

        doc.save(output_file_name, compression_effort=5)
        print(f"Redacted PDF saved as {output_file_name}")

    def redact_all_files_in_dir(self, base_path: Path, text_to_redact: str, output_file_suffix: str):
        for file in base_path.rglob("*.pdf"):
            file_stem = file.stem
            self.redact_text(file, text_to_redact, file.with_name(file_stem + f"_{output_file_suffix}.pdf"))


def main():
    base_path = Path.joinpath(Path("G:\\"), Path("Meu Drive"), Path("Desafio Detox 15 dias"))
    text_to_redact = os.environ.get("TEXT_TO_REDACT", "")
    text_redactor = TextRedactor()
    text_redactor.redact_all_files_in_dir(base_path, text_to_redact=text_to_redact, output_file_suffix="redacted")


if __name__ == "__main__":
    load_dotenv()
    main()
