from pathlib import Path
from typing import Union

import fitz  # pymupdf
from loguru import logger


class TextRedactor:
    """Redact a text from a pdf file

    Methods:

    - redact_text(file_path: Path, text_to_redact: str, output_file_name:Path) -> bool

    - redact_all_files_in_dir(base_path: Path, text_to_redact: str, output_file_suffix: str) -> None
    """

    def redact_text(self, file_path: Path, text_to_redact: str, output_file_name: Path) -> Union[bool, None]:
        """Open the document and redact the text

        Args:
            file_path (Path): PDF file path.
            text_to_redact (str): Text or phrase to be redacted in every page of pdf file.
            output_file_name (Path): PDF file name (include .pdf) to be saved after redact.

        Returns:
            bool: If successfully redacts the text in pdf.
            None: Cannot find text in any page.

        Examples:
            >>> from redact_pdf.redact import TextRedactor
            >>> tr = TextRedactor()
            >>> pdf_file = Path("path/to/input.pdf")
            >>> TEXT_TO_REDACT = "Confidential"
            >>> save_path = Path("path/to/output.pdf")
            >>> tr.redact_text(file_path=pdf_file, text_to_redact=TEXT_TO_REDACT, output_file_name=save_path)
            True
        """
        doc = None
        try:
            logger.info("Opening file...")
            doc = fitz.open(file_path)
            logger.success("wFile Opened.")

            redacted = False

            for i in range(doc.page_count):
                logger.info("Checking page {}", i + 1)
                page = doc.load_page(i)
                redaction_list = page.search_for(text_to_redact, quads=True)

                if redaction_list:  # Ensure results were found before proceeding
                    logger.info("Found text at page {}", i + 1)
                    redacted = True
                    for redact_area in redaction_list:
                        page.add_redact_annot(redact_area, "REDACTED")
                        page.apply_redactions()  # Apply redactions
                    logger.success("Applied Redactions.")

            if redacted:
                logger.info("Saving file...")
                doc.save(output_file_name, compression_effort=5)
                logger.info(f"Successfully redacted and saved: {output_file_name}")

                return True
            else:
                logger.info(f"No text found to redact in: {file_path}")
                return None
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return False
        finally:
            if doc is not None:
                doc.close()

    def redact_all_files_in_dir(self, base_path: Path, text_to_redact: str, output_file_suffix: str) -> None:
        """Redact all files in a local directory

        Args:
            base_path (Path): Base directory to find all *.pdf files (recursively)
            text_to_redact (str): Text or phrase to be redacted in every page of pdf file.
            output_file_suffix (str): Suffix to append to original file name to be saved.

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
        processed_count = 0
        error_count = 0
        try:
            pdf_files = list(base_path.rglob("*.pdf"))
            logger.info(f"Found {len(pdf_files)} PDF files in directory {base_path}")

            for file in pdf_files:
                output_file = file.with_name(file.stem + f"_{output_file_suffix}.pdf")

                result = self.redact_text(file, text_to_redact, output_file_name=output_file)
                if result or result is None:
                    processed_count += 1
                else:
                    error_count += 1

            logger.info(f"Processing complete. Successfully processed: {processed_count}, Errors: {error_count}")

        except Exception as e:
            logger.error(f"Fatal error during processing: {e}")
