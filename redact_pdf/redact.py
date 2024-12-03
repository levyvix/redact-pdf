import os
from pathlib import Path

import fitz  # pymupdf
from dotenv import load_dotenv
from loguru import logger


class TextRedactor:
    """Redact a text from a pdf file

    Methods:

    - redact_text(file_path: Path, text_to_redact: str, output_file_name:Path) -> None

    - redact_all_files_in_dir(base_path: Path, text_to_redact: str, output_file_suffix: str) -> None
    """

    def redact_text(self, file_path: Path, text_to_redact: str, output_file_name: Path) -> None:
        """Open the document and redact the text

        Args:
            file_path (Path): PDF file path.
            text_to_redact (str): Text or phrase to be redacted in every page of pdf file.
            output_file_name (Path): PDF file name (include .pdf) to be saved after redact.

        Returns:
            None

        Examples:
            >>> from redact_pdf.redact import TextRedactor
            >>> tr = TextRedactor()
            >>> pdf_file = Path("path/to/input.pdf")
            >>> TEXT_TO_REDACT = "Confidential"
            >>> save_path = Path("path/to/output.pdf")
            >>> tr.redact_text(file_path=pdf_file, text_to_redact=TEXT_TO_REDACT, output_file_name=save_path)
        """
        logger.info("Opening file...")
        doc = fitz.open(file_path)
        logger.success("File Opened.")

        for i in range(doc.page_count):
            logger.info("Checking page {}", i + 1)
            page = doc.load_page(i)
            rl = page.search_for(text_to_redact, quads=True)

            if rl:  # Ensure results were found before proceeding
                logger.info("Found text at page {}", i + 1)
                page.add_redact_annot(rl[0])  # Add redaction annotation for the first match
                page.apply_redactions()  # Apply redactions
                logger.success("Applied Redactions.")

        logger.info("Saving file...")
        doc.save(output_file_name, compression_effort=5)
        logger.success("Redacted PDF saved as {}", output_file_name)

    def redact_all_files_in_dir(self, base_path: Path, text_to_redact: str, output_file_suffix: str) -> None:
        """Redact all files in a local directory

        Args:
            base_path (Path): Base directory to find all *.pdf files (recursively)
            text_to_redact (str): Text or phrase to be redacted in every page of pdf file.
            output_file_suffix (Path): Suffix to append to original file name to be saved.

        Returns:
            None

        Examples:
            >>> from redact_pdf.redact import TextRedactor
            >>> tr = TextRedactor()
            >>> base_path = Path("path/to/files/")
            >>> TEXT_TO_REDACT = "Confidential"
            >>> suffix = "redacted"
            >>> tr.redact_all_files_in_dir(base_path=base_path, text_to_redact=TEXT_TO_REDACT, output_file_suffix=suffix)
        """
        for file in base_path.rglob("*.pdf"):
            file_stem = file.stem
            self.redact_text(file, text_to_redact, file.with_name(file_stem + f"_{output_file_suffix}.pdf"))


if __name__ == "__main__":
    load_dotenv()
    base_path = Path.joinpath(Path("G:\\"), Path("Meu Drive"), Path("Desafio Detox 15 dias"))
    text_to_redact = os.environ.get("TEXT_TO_REDACT", "")
    text_redactor = TextRedactor()
    text_redactor.redact_all_files_in_dir(base_path, text_to_redact=text_to_redact, output_file_suffix="redacted")
