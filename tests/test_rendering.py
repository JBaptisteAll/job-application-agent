"""Rendering checks: PDF page count and ATS reading order.

Both templates are rendered with the fictional person of the fixtures,
converted to PDF with LibreOffice, then read back with pypdf, the way an
ATS would extract the text.

The tests are skipped when LibreOffice is not installed, so `uv run pytest`
still works on any machine. In CI they must run: a missing LibreOffice
fails the tests there instead of skipping them.
"""

import json
import os
import shutil
import subprocess
from datetime import date
from pathlib import Path

import pytest
from pypdf import PdfReader

from job_application_agent.cover_letter import FIXED_TEXTS, render_cover_letter
from job_application_agent.cv import SECTION_TITLES, render_cv

FIXTURES = Path(__file__).parent / "fixtures"
LETTER_DATE = date(2026, 11, 22)
WINDOWS_SOFFICE = Path(r"C:\Program Files\LibreOffice\program\soffice.exe")


def find_soffice() -> str | None:
    """Return the LibreOffice command, or None if it is not installed."""
    for name in ("soffice", "libreoffice"):
        command = shutil.which(name)
        if command:
            return command
    if WINDOWS_SOFFICE.exists():
        return str(WINDOWS_SOFFICE)
    return None


SOFFICE = find_soffice()

if SOFFICE is None and os.environ.get("CI"):
    pytest.fail("LibreOffice is required in CI for the rendering tests", pytrace=False)

pytestmark = pytest.mark.skipif(SOFFICE is None, reason="LibreOffice not installed")


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def convert_to_pdf(docx_path: Path, work_dir: Path) -> Path:
    """Convert a .docx file to PDF with LibreOffice in headless mode.

    A dedicated LibreOffice profile in `work_dir` keeps the conversion
    independent from any LibreOffice window the user has open.
    """
    profile = (work_dir / "lo_profile").as_uri()
    subprocess.run(
        [
            SOFFICE,
            f"-env:UserInstallation={profile}",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(work_dir),
            str(docx_path),
        ],
        check=True,
        capture_output=True,
        timeout=180,
    )
    pdf_path = work_dir / f"{docx_path.stem}.pdf"
    assert pdf_path.exists(), f"LibreOffice did not create {pdf_path.name}"
    return pdf_path


def extract_text(pdf_path: Path) -> str:
    """Extract the text of every page, with all whitespace reduced to single spaces.

    Line breaks depend on the font and the PDF reader, so they are not compared.
    """
    reader = PdfReader(pdf_path)
    text = " ".join(page.extract_text() for page in reader.pages)
    return " ".join(text.split())


def assert_in_order(text: str, parts: list[str]) -> None:
    """Check that each part appears in `text`, after the previous one."""
    position = 0
    for part in parts:
        expected = " ".join(part.split())
        found = text.find(expected, position)
        assert found != -1, f"{expected!r} is missing or out of order"
        position = found + len(expected)


@pytest.fixture(scope="module")
def cv_content() -> dict:
    return load_fixture("cv_fictif.json")


@pytest.fixture(scope="module")
def letter_content() -> dict:
    return load_fixture("lettre_fictive.json")


@pytest.fixture(scope="module")
def cv_pdf(cv_content, tmp_path_factory) -> Path:
    work_dir = tmp_path_factory.mktemp("cv")
    docx_path = render_cv(cv_content, work_dir / "cv.docx")
    return convert_to_pdf(docx_path, work_dir)


@pytest.fixture(scope="module")
def letter_pdf(letter_content, tmp_path_factory) -> Path:
    work_dir = tmp_path_factory.mktemp("letter")
    docx_path = render_cover_letter(
        letter_content, work_dir / "lettre.docx", letter_date=LETTER_DATE
    )
    return convert_to_pdf(docx_path, work_dir)


def test_cv_fits_on_one_page(cv_pdf):
    assert len(PdfReader(cv_pdf).pages) == 1


def test_cover_letter_fits_on_one_page(letter_pdf):
    assert len(PdfReader(letter_pdf).pages) == 1


def test_cv_text_follows_reading_order(cv_pdf, cv_content):
    titles = SECTION_TITLES["fr"]
    parts = [
        cv_content["nom"],
        cv_content["titre_cv"],
        titles["profil"],
        titles["competences"],
        titles["experience"],
    ]
    for experience in cv_content["experiences"]:
        parts += [experience["intitule"], experience["dates"], experience["entreprise"]]
    parts.append(titles["projets"])
    parts += [project["nom"] for project in cv_content["projets"]]
    parts += [titles["formation"], titles["langues"], titles["references"]]

    assert_in_order(extract_text(cv_pdf), parts)


def test_cover_letter_text_follows_reading_order(letter_pdf, letter_content):
    texts = FIXED_TEXTS["fr"]
    parts = [
        letter_content["nom"],
        letter_content["email"],
        letter_content["entreprise"],
        "le 22 novembre 2026",
        f"{texts['objet_prefixe']} {letter_content['titre']}",
        texts["salutation"],
    ]
    # The start of each paragraph is enough to check the order.
    parts += [paragraph[:40] for paragraph in letter_content["corps"]]
    parts += [texts["conclusion"], texts["formule"]]

    assert_in_order(extract_text(letter_pdf), parts)
