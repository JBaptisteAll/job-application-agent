"""Fill the cover letter template with the content written for a job offer.

The body is written upstream, under the rules of `docs/editable-areas.md`.
This module places it in a classic French letter layout, and builds the
fixed parts itself: sender and recipient blocks, date line, salutation,
conclusion and closing formula.
"""

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from docxtpl import DocxTemplate

TEMPLATE_PATH = Path(__file__).parent / "templates" / "cover_letter_template.docx"

MAX_BODY_PARAGRAPHS = 3

FIXED_TEXTS = {
    "fr": {
        "objet": "Objet :",
        "objet_prefixe": "Candidature au poste de",
        "recruteur_defaut": "Service recrutement",
        "salutation": "Madame, Monsieur,",
        "conclusion": "Je serais disponible pour un échange à votre convenance.",
        "formule": (
            "Je vous prie d'agréer, Madame, Monsieur, "
            "l'expression de mes salutations distinguées."
        ),
    },
    "en": {
        "objet": "Subject:",
        "objet_prefixe": "Application for the position of",
        "recruteur_defaut": "Recruitment team",
        "salutation": "Dear Hiring Manager,",
        "conclusion": "I would be glad to discuss this at your convenience.",
        "formule": "Kind regards,",
    },
}

# Month names are written here rather than taken from the system locale,
# so the result is the same on every machine.
MONTHS = {
    "fr": [
        "janvier",
        "février",
        "mars",
        "avril",
        "mai",
        "juin",
        "juillet",
        "août",
        "septembre",
        "octobre",
        "novembre",
        "décembre",
    ],
    "en": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
}


def today() -> date:
    """Today's date in the user's local time zone."""
    return datetime.now(UTC).astimezone().date()


def format_date_line(letter_date: date, place: str | None, language: str) -> str:
    """Build the place and date line, such as "Lyon, le 22 novembre 2026".

    `place` is None when the displayed location is a country only:
    the line then shows the date alone.
    """
    month = MONTHS[language][letter_date.month - 1]
    if language == "fr":
        day = "1er" if letter_date.day == 1 else str(letter_date.day)
        text = f"le {day} {month} {letter_date.year}"
        return f"{place}, {text}" if place else text[0].upper() + text[1:]
    text = f"{letter_date.day} {month} {letter_date.year}"
    return f"{place}, {text}" if place else text


def render_cover_letter(
    content: dict[str, Any],
    output_path: Path,
    language: str = "fr",
    letter_date: date | None = None,
    template_path: Path = TEMPLATE_PATH,
) -> Path:
    """Render the cover letter template with `content` and save it to `output_path`.

    `language` is the document language, which follows the job offer.
    `letter_date` defaults to today; tests pass a fixed date.
    """
    if language not in FIXED_TEXTS:
        raise ValueError(f"Unsupported language: {language!r}")
    body = content["corps"]
    if not 1 <= len(body) <= MAX_BODY_PARAGRAPHS:
        raise ValueError(
            f"The body must have 1 to {MAX_BODY_PARAGRAPHS} paragraphs, got {len(body)}"
        )

    texts = FIXED_TEXTS[language]
    sender = [
        content.get("ville"),
        content.get("telephone"),
        content.get("email"),
    ]
    recipient = [
        content.get("recruteur") or texts["recruteur_defaut"],
        content.get("ville_poste"),
    ]
    context = {
        "t": texts,
        "nom": content["nom"],
        "expediteur": [line for line in sender if line],
        "entreprise": content["entreprise"],
        "destinataire": [line for line in recipient if line],
        "ligne_date": format_date_line(
            letter_date or today(), content.get("lieu_date"), language
        ),
        "objet": f"{texts['objet_prefixe']} {content['titre']}",
        "corps": body,
    }

    template = DocxTemplate(template_path)
    # autoescape keeps characters such as "&" and "<" in the document.
    template.render(context, autoescape=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    template.save(output_path)
    return output_path
