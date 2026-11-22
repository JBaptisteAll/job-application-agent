"""Tests for the CV template, rendered with a fictional person."""

import json
from pathlib import Path

import pytest
from docx import Document
from docxtpl import DocxTemplate

from job_application_agent.cv import MAX_MISC_LINES, TEMPLATE_PATH, render_cv

FIXTURES = Path(__file__).parent / "fixtures"

EXPECTED_VARIABLES = {
    "t",
    "nom",
    "titre_cv",
    "coordonnees",
    "profil",
    "competences",
    "certifications",
    "experiences",
    "projets",
    "formation",
    "langues",
    "divers",
    "references",
}


@pytest.fixture
def content() -> dict:
    return json.loads((FIXTURES / "cv_fictif.json").read_text(encoding="utf-8"))


def document_text(path: Path) -> str:
    return "\n".join(paragraph.text for paragraph in Document(path).paragraphs)


def test_template_declares_every_placeholder():
    template = DocxTemplate(TEMPLATE_PATH)
    assert template.get_undeclared_template_variables() == EXPECTED_VARIABLES


def test_render_contains_all_selected_content(content, tmp_path):
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    assert "Camille Martin" in text
    for experience in content["experiences"]:
        assert experience["intitule"] in text
        for point in experience["points"]:
            assert point in text
    for project in content["projets"]:
        assert project["nom"] in text
        assert project["synthese"] in text
    for line in content["divers"]:
        assert line["texte"] in text
    assert "Références disponibles sur demande" in text
    assert "{{" not in text
    assert "{%" not in text


def test_contact_line_uses_short_link_labels(content, tmp_path):
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    contact_line = text.splitlines()[2]
    assert "LinkedIn  |  GitHub  |  Portfolio" in contact_line
    assert "https://" not in contact_line


def test_special_characters_are_kept(content, tmp_path):
    content["titre_cv"] = "Data Analyst - R&D <Pricing> & Revenue"
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    assert "Data Analyst - R&D <Pricing> & Revenue" in text
    assert "Hôtel Fictif & Spa" in text


def test_experience_with_no_bullet_point_keeps_its_line(content, tmp_path):
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    assert "Conseillère commerciale" in text
    assert "Croisières Exemple · Marseille" in text


def test_optional_lines_are_hidden_when_empty(content, tmp_path):
    content["certifications"] = ""
    content["divers"] = []
    content["references"] = False
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    assert "Certifications" not in text
    assert "Bénévolat" not in text
    assert "Références disponibles sur demande" not in text
    assert "Langues : " in text


def test_hidden_contact_value_leaves_no_extra_separator(content, tmp_path):
    content["contact"] = [
        item for item in content["contact"] if item["label"] != "Lyon"
    ]
    text = document_text(render_cv(content, tmp_path / "cv.docx"))

    contact_line = text.splitlines()[2]
    assert "Lyon" not in contact_line
    assert "|  |" not in contact_line


def test_english_section_titles(content, tmp_path):
    text = document_text(render_cv(content, tmp_path / "cv.docx", language="en"))

    assert "PROFESSIONAL EXPERIENCE" in text
    assert "References available on request" in text
    assert "EXPÉRIENCE PROFESSIONNELLE" not in text


def test_unsupported_language_is_rejected(content, tmp_path):
    with pytest.raises(ValueError, match="Unsupported language"):
        render_cv(content, tmp_path / "cv.docx", language="de")


def test_too_many_miscellaneous_lines_are_rejected(content, tmp_path):
    content["divers"] = [{"libelle": "Concours", "texte": "Exemple"}] * (
        MAX_MISC_LINES + 1
    )
    with pytest.raises(ValueError, match="miscellaneous lines"):
        render_cv(content, tmp_path / "cv.docx")
