# Onboarding

> Status: phase 1 specification. Related issues: #16 (this document), #14 (`profil.md` structure), #15 (archive files), #54 (approved cover letters as style models), #55 (English interface texts).

Onboarding is the short conversation the agent has with the user on the first run. It collects what the LinkedIn archive cannot tell, and writes the answers into `profil.md`. This document defines when onboarding runs, the interface language, the questions, the expected answer formats, and how the writing style is captured.

## Principles

1. **Ask only what the archive cannot tell.** Everything the archive contains is pre-filled first (see [`archive-files.md`](archive-files.md)). The agent never asks for a value it already has.
2. **Answers go into `profil.md`.** The conversation is only a way to fill the file. `profil.md` remains the single source of truth and the only place to correct a value (see [`profil-structure.md`](profil-structure.md)). Every answer is written with `<!-- src: user -->`.
3. **Never blocking.** A required question the user skips, or a run with no one to answer (for example a script), leaves the field as `[À COMPLÉTER]`. The user can fill it later in `profil.md`.
4. **A human always decides.** The agent asks, writes and reminds. It never acts on the user's behalf.
5. **Two separate languages.** The *interface language* is chosen once, at onboarding, and applies to everything the user reads: questions, `profil.md` labels, reminders and error messages. The *document language* always follows the language of the job offer. An English-speaking user can receive a French CV for a French offer.

## When onboarding runs

- **First run:** the agent parses the archive, pre-fills `profil.md`, asks the questions below, writes the answers, then stops and asks the user to review the file (`reviewed: false`). No CV or cover letter is generated before the review.s
- **Later runs:** no questions. The user edits `profil.md` directly. If a new archive adds an entry with missing values (for example a new education without a field of study), the agent writes `[À COMPLÉTER]` and lists the fields to complete, without asking.

## Interface language

### Question 0

Asked first, in both languages, before anything else:

> Dans quelle langue veux-tu utiliser l'outil ? / Which language do you want to use the tool in? (`français` / `English`)

- The answer is stored in the front matter of `profil.md` as `interface_language: fr` or `interface_language: en`.
- With no answer, the default is `fr`, since the tool targets the French job market for now.
- The user can change the value later in `profil.md`. The agent then rewrites the labels in the new language on the next run, without changing any value.

### Label mapping

Code never searches for a label written in plain text, such as `Postes visés :`. Every field has a fixed internal key, and a mapping table gives its label in each language:

| Key | `fr` | `en` |
| --- | --- | --- |
| `target_roles` | Postes visés | Target roles |
| `contract_types` | Type de contrat | Contract types |
| `search_zones` | Zones de recherche | Search areas |

The full table covers every field of `profil.md`. A renamed or translated label therefore never breaks the parser.

### Scope of this document

This document defines the questions in French. The English version of every user-facing text (questions, `profil.md` labels, the "About this file" text, reminders and error messages) is tracked in #55. Until then, the interface is available in French only, and question 0 is not asked.

## Special answers

These answers are accepted for every question where they make sense:

| Answer | Effect | Allowed for |
| --- | --- | --- |
| `passer` | Required question: the field becomes `[À COMPLÉTER]`. Optional question: the field becomes `aucun`, which never blocks generation. | All questions except 0 |
| `ne pas afficher` | The field becomes `[NE PAS AFFICHER]` and never appears in a document | Questions 8, 9 and 10 |

**Invalid answer:** the agent rephrases the question once, with an example. If the second answer is still invalid, it writes `[À COMPLÉTER]` for a required question, or `aucun` for an optional one, and moves on. It never loops.

## Questions

Asked in this order, after question 0. The search questions come first, because they matter most and the user is most attentive at the start.

### A. Recherche (section 2, never shown on a CV)

| # | Question asked | Field | Expected format | Required |
| --- | --- | --- | --- | --- |
| 1 | Quels postes vises-tu ? (3 au maximum, par ordre de priorité) | Postes visés | Comma-separated list, 1 to 3 titles | Yes |
| 2 | Quels types de contrat ? | Type de contrat | One or more of `CDI`, `CDD`, `freelance`, `alternance`, `stage` | Yes |
| 3 | Où cherches-tu ? | Zones de recherche | One or more zones, each with its CV location (see below) | Yes |
| 4 | Quel rythme de télétravail ? | Télétravail | One of `sur site`, `hybride`, `full remote`, `indifférent` | Yes |
| 5 | Quelle est ta disponibilité ? | Disponibilité | One of `immédiate`, `préavis` | Yes |
| 6 | As-tu une ambition à long terme ? | Ambition à long terme | Free text | No |
| 7 | Y a-t-il des postes ou des entreprises que tu ne veux pas ? | Ce que je ne veux pas | Free text list | No |

#### Question 3: search zones

A user can search in several areas, and the location shown on the CV depends on the area of the job offer. Each zone therefore has two values:

| Value | Example | Shown on the CV |
| --- | --- | --- |
| Zone | `Bordeaux et alentours` | No |
| Localisation (CV) | `Bordeaux (mobilité)` | Yes |

Flow:

1. The agent proposes the city found in the archive as the first zone: « Ton profil LinkedIn indique « Paris ». Zone 1 : Île-de-France, affichée « Paris » sur ton CV ? (`oui` ou ta correction) »
2. Then it asks: « Une autre zone ? (`non`, ou `zone → localisation`) ». It repeats until the user answers `non`, with 5 zones at most.
3. When the CV location is a place where the user does not live yet, the agent suggests adding « (mobilité) ». The user decides.

Rules for job offers:

- An offer inside at least one zone uses the CV location of that zone.
- An offer outside every zone is **flagged, never rejected**: the analysis states that it is out of the search area, and the user decides. Its CV uses the location of the first zone.
- Zones are free text, so the AI judges whether an offer falls inside a zone.

### B. Compléments de profil (not in the archive)

| # | Question asked | Field | Expected format | Required |
| --- | --- | --- | --- | --- |
| 8 | Quelle est l'adresse de ton profil LinkedIn ? | LinkedIn (section 1) | URL starting with `https://www.linkedin.com/in/` | Yes |
| 9 | As-tu un profil GitHub ? | GitHub (section 1) | URL starting with `https://github.com/` | Yes |
| 10 | Quel est le domaine d'études de « {formation} » ? | Domaine (section 5) | Free text, asked once per education entry. Skipped if there is none. | Yes |

### C. Style d'écriture (section 12)

| # | Question asked | Field | Expected format | Required |
| --- | --- | --- | --- | --- |
| 11 | Sur quoi puis-je m'appuyer pour reprendre ton style d'écriture ? | Sources de style | One of `posts`, `lettres`, `les deux`, `aucun` | No |

See [Writing style](#writing-style) below.

## Writing style

Cover letters written by AI tend to sound the same. The agent can instead follow the user's own style, taken from texts the user wrote.

### Sources

| Answer | Source | What it brings |
| --- | --- | --- |
| `posts` | `Shares.csv` from the archive | Vocabulary and rhythm |
| `lettres` | 2 or 3 former cover letters (PDF or DOCX) placed by the user in `cover_letters/` | Register and structure |
| `les deux` | Both | Letters for register and structure, posts for vocabulary and rhythm |
| `aucun` | None | Section 12 is left out, and cover letters use a neutral professional style |

If the user answers `lettres` or `les deux` and `cover_letters/` is empty, the agent says so and builds the portrait at the next run where letters are present.

### How posts are used

- `Shares.csv` is read **only** if the user answered `posts` or `les deux`.
- Code selects up to 10 recent posts with at least 500 characters written by the user. Reposts with no text of their own are ignored.
- Code removes emojis, hashtags and links before any AI call.
- A LinkedIn post is not a cover letter: posts give vocabulary and rhythm only. Hooks, emojis and hashtags never reach a cover letter, which keeps a formal register.

### Style portrait

- The AI reads the selected sources **once** and writes a short style portrait in section 12 of `profil.md`, with `<!-- src: ai -->`: tone, sentence length, recurring words, structure of a letter.
- The user reviews it like the rest of the file.
- Cover letters are written from the portrait, **never from the sources themselves**.
- **Style only, never content.** No sentence, company name, recipient or fact from a source text is ever copied into a new letter.
- The portrait is rebuilt when the sources change, and the agent shows the user what changed.

### Privacy

`cover_letters/` contains personal data (companies, recipients, addresses). Like the archive and `profil.md`, it is excluded by `.gitignore` and blocked by the pre-commit hook that prevents committing personal data files.

### Later: approved generated letters

After each cover letter is generated, the agent displays a reminder: the user can copy the letter into `cover_letters/` if they want it to serve as a style model. The agent never copies it itself. Rules for these letters, including how the agent avoids imitating its own style, are tracked in #54.

## Example

An extract of `profil.md` after onboarding. The person and all values are fictional.

```markdown
---
schema_version: 1
interface_language: fr
archive_date: 2026-11-16
generated_on: 2026-11-20
reviewed: false
---

## 2. Recherche

- Postes visés : Data Analyst, Analytics Engineer <!-- src: user -->
- Type de contrat : CDI <!-- src: user -->
- Télétravail : hybride <!-- src: user -->
- Disponibilité : préavis <!-- src: user -->
- Ambition à long terme : Data Engineer <!-- src: user -->
- Ce que je ne veux pas : aucun <!-- src: user -->

### Zones de recherche

| Zone | Localisation (CV) |
| --- | --- |
| Lyon et alentours | Lyon <!-- src: user --> |
| Grenoble | Grenoble (mobilité) <!-- src: user --> |

## 12. Style d'écriture

- Sources : posts <!-- src: user -->

**Portrait** <!-- src: ai -->
Ton direct et chaleureux. Phrases courtes, souvent introduites par un verbe d'action. Exemples concrets chiffrés plutôt qu'adjectifs.
```
