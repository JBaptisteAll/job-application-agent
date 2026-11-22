"""Fill the CV template with the content selected for a job offer.

The content is selected and written upstream, under the rules of
`docs/editable-areas.md`. This module only places it in the template.
"""

from pathlib import Path
from typing import Any

from docxtpl import DocxTemplate, RichText

TEMPLATE_PATH = Path(__file__).parent / "templates" / "cv_template.docx"

MAX_MISC_LINES = 2

SECTION_TITLES = {
    "fr": {
        "profil": "PROFIL",
        "competences": "COMPÉTENCES",
        "certifications": "Certifications",
        "experience": "EXPÉRIENCE PROFESSIONNELLE",
        "projets": "PROJETS",
        "formation": "FORMATION",
        "langues": "LANGUES & DIVERS",
        "langues_label": "Langues",
        "references": "Références disponibles sur demande",
    },
    "en": {
        "profil": "PROFILE",
        "competences": "SKILLS",
        "certifications": "Certifications",
        "experience": "PROFESSIONAL EXPERIENCE",
        "projets": "PROJECTS",
        "formation": "EDUCATION",
        "langues": "LANGUAGES & MISCELLANEOUS",
        "langues_label": "Languages",
        "references": "References available on request",
    },
}

# Contact line style: grey text, accent-coloured links, 9.5 pt (docxtpl sizes are half-points).
_CONTACT_SIZE = 19
_GREY = "555555"
_ACCENT = "1F3A5F"
_SEPARATOR = "  |  "


def build_contact_line(template: DocxTemplate, items: list[dict[str, Any]]) -> RichText:
    """Build the single contact line.

    Each item has a `label` and an optional `url`. Items with a URL become
    short clickable labels, such as "LinkedIn". Hidden values are simply not
    passed, so no separator is left behind.
    """
    line = RichText()
    for index, item in enumerate(items):
        if index:
            line.add(_SEPARATOR, color=_GREY, size=_CONTACT_SIZE)
        url = item.get("url")
        if url:
            line.add(
                item["label"],
                url_id=template.build_url_id(url),
                color=_ACCENT,
                underline=True,
                size=_CONTACT_SIZE,
            )
        else:
            line.add(item["label"], color=_GREY, size=_CONTACT_SIZE)
    return line


def render_cv(
    content: dict[str, Any],
    output_path: Path,
    language: str = "fr",
    template_path: Path = TEMPLATE_PATH,
) -> Path:
    """Render the CV template with `content` and save it to `output_path`.

    `language` is the document language, which follows the job offer.
    """
    if language not in SECTION_TITLES:
        raise ValueError(f"Unsupported language: {language!r}")
    if len(content.get("divers", [])) > MAX_MISC_LINES:
        raise ValueError(f"At most {MAX_MISC_LINES} miscellaneous lines are allowed")

    template = DocxTemplate(template_path)
    context = {
        **content,
        "t": SECTION_TITLES[language],
        "coordonnees": build_contact_line(template, content["contact"]),
    }
    # autoescape keeps characters such as "&" and "<" in the document.
    template.render(context, autoescape=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    template.save(output_path)
    return output_path
