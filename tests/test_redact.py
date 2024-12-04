import os
from pathlib import Path

from pypdf import PdfReader

from redact_pdf.redact import TextRedactor


def clean_pdf_file(path: Path):
    os.remove(path)


def test_create_new_pdf():
    pdf_file = Path(__file__).parent / "pdf_test.pdf"
    save_path = Path(__file__).parent / "pdf_test_redacted.pdf"
    if save_path.exists():
        os.remove(save_path)

    text_redactor = TextRedactor()

    text_redactor.redact_text(
        file_path=pdf_file,
        text_to_redact="FULANO DA SILVA",
        output_file_name=save_path,
    )

    assert save_path.exists()


def test_not_create_new_pdf():
    pdf_file = Path(__file__).parent / "pdf_test.pdf"
    save_path = Path(__file__).parent / "pdf_test_redacted.pdf"
    if save_path.exists():
        os.remove(save_path)

    text_redactor = TextRedactor()

    text_redactor.redact_text(
        file_path=pdf_file,
        text_to_redact="XXX",
        output_file_name=save_path,
    )

    assert not save_path.exists()


def test_redact_text():
    pdf_file = Path(__file__).parent / "pdf_test.pdf"
    save_path = Path(__file__).parent / "pdf_test_redacted.pdf"
    if save_path.exists():
        os.remove(save_path)

    TEXT_TO_REDACT = "FULANO DA SILVA"
    text_redactor = TextRedactor()

    text_redactor.redact_text(
        file_path=pdf_file,
        text_to_redact=TEXT_TO_REDACT,
        output_file_name=save_path,
    )

    # open pdf and search for text
    failed = False

    reader = PdfReader(save_path)

    for page in reader.pages:
        text = page.extract_text()

        if TEXT_TO_REDACT in text:
            failed = True

    assert not failed


def test_redact_all_file_in_dir():
    base_path = Path(__file__).parent
    suffix = "redacted"

    for file in base_path.rglob(f"*_{suffix}.pdf"):
        os.remove(file)

    # get all pdf files
    all_pdf_files = list(base_path.rglob("*.pdf"))
    print(list(all_pdf_files))

    tr = TextRedactor()
    tr.redact_all_files_in_dir(
        base_path=base_path,
        text_to_redact="FULANO DA SILVA",
        output_file_suffix=suffix,
    )

    checks = []
    for file in all_pdf_files:
        # checks.append(Path(file.stem + f"_{suffix}.pdf").exists())
        checks.append((Path(__file__).parent / Path(file.stem + f"_{suffix}.pdf")).exists())

    assert all(checks)
