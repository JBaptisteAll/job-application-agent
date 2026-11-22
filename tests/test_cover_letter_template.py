"""Tests for the cover letter template, rendered with a fictional person."""

import json
from datetime import date
from pathlib import Path

import pytest
from docx import Document
from docxtpl import DocxTemplate

from job_application_agent.cover_letter import (
    FIXED_TEXTS,
    MAX_BODY_PARAGRAPHS,
    TEMPLATE_PATH,
    format_date_line,
    render_cover_letter,
)

FIXTURES = Path(__file__).parent / "fixtures"
LETTER_DATE = date(2026, 11, 22)

EXPECTED_VARIABLES = {
    "t",
    "nom",
    "expediteur",
    "entreprise",
    "destinataire",
    "ligne_date",
    "objet",
    "corps",
}


@pytest.fixture
def content() -> dict:
    return json.loads((FIXTURES / "lettre_fictive.json").read_text(encoding="utf-8"))


def render_text(content: dict, tmp_path: Path, language: str = "fr") -> str:
    path = render_cover_letter(
        content, tmp_path / "lettre.docx", language=language, letter_date=LETTER_DATE
    )
    return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)


def test_template_declares_every_placeholder():
    template = DocxTemplate(TEMPLATE_PATH)
    assert template.get_undeclared_template_variables() == EXPECTED_VARIABLES


def test_french_letter_contains_every_part(content, tmp_path):
    text = render_text(content, tmp_path)
    lines = text.splitlines()

    assert lines[:4] == [
        "Camille Martin",
        "Lyon",
        "06 00 00 00 00",
        "camille.martin@example.com",
    ]
    assert "Exemple Voyages & Co\nService recrutement\nVilleurbanne" in text
    assert "Lyon, le 22 novembre 2026" in text
    assert "Objet : Candidature au poste de Data Analyst - Pricing & Revenue" in text
    for paragraph in content["corps"]:
        assert paragraph in text
    assert "{{" not in text
    assert "{%" not in text


def test_fixed_texts_are_used_word_for_word(content, tmp_path):
    for language in ("fr", "en"):
        text = render_text(content, tmp_path, language)
        texts = FIXED_TEXTS[language]
        assert texts["salutation"] in text
        assert texts["conclusion"] in text
        assert texts["formule"] in text


def test_english_letter(content, tmp_path):
    text = render_text(content, tmp_path, language="en")

    assert "Recruitment team" in text
    assert "Lyon, 22 November 2026" in text
    assert "Subject: Application for the position of" in text


def test_letter_has_no_links(content, tmp_path):
    text = render_text(content, tmp_path)

    assert "http" not in text
    assert "LinkedIn" not in text


def test_recruiter_name_replaces_default(content, tmp_path):
    content["recruteur"] = "Alex Dupont"
    text = render_text(content, tmp_path)

    assert "Alex Dupont" in text
    assert "Service recrutement" not in text
    assert "Madame, Monsieur," in text


def test_missing_values_remove_their_lines(content, tmp_path):
    content["telephone"] = None
    content["ville_poste"] = None
    text = render_text(content, tmp_path)

    assert "06 00 00 00 00" not in text
    assert "Villeurbanne" not in text
    assert "Lyon\ncamille.martin@example.com" in text


@pytest.mark.parametrize(
    ("letter_date", "place", "language", "expected"),
    [
        (date(2026, 11, 22), "Lyon", "fr", "Lyon, le 22 novembre 2026"),
        (date(2026, 12, 1), "Lyon", "fr", "Lyon, le 1er décembre 2026"),
        (date(2026, 8, 15), None, "fr", "Le 15 août 2026"),
        (date(2026, 11, 22), "Lyon", "en", "Lyon, 22 November 2026"),
        (date(2026, 12, 1), None, "en", "1 December 2026"),
    ],
)
def test_date_line(letter_date, place, language, expected):
    assert format_date_line(letter_date, place, language) == expected


@pytest.mark.parametrize("count", [0, MAX_BODY_PARAGRAPHS + 1])
def test_wrong_number_of_paragraphs_is_rejected(content, tmp_path, count):
    content["corps"] = ["Paragraphe."] * count
    with pytest.raises(ValueError, match="paragraphs"):
        render_text(content, tmp_path)


def test_unsupported_language_is_rejected(content, tmp_path):
    with pytest.raises(ValueError, match="Unsupported language"):
        render_text(content, tmp_path, language="de")
