# `profil.md` structure

> Status: phase 1 specification. Related issues: #14 (this document), #15 (archive files), #16 (onboarding), #24 (contradictions), #25 (condensed texts and translations), #55 (English interface texts), #57 (experience and project files), #18 (CV template).

`profil.md` is the main profile file of the user. Every later step reads it: CV, cover letter and offer scoring. Experiences and projects are stored in two companion files, `experiences.md` and `projets.md` (see [`experience-project-files.md`](experience-project-files.md)). This document defines its layout, its sections and fields, the source of each value, and how missing or hidden values are handled.

## Principles

1. **Single source of truth.** `profil.md`, `experiences.md` and `projets.md` replace the three files of the current workflow (see [Replaced files](#replaced-files)). Every piece of information is written in one place only: `profil.md` points to the two other files instead of repeating their content.
2. **Pre-filled, then corrected by the user.** The agent fills everything it can from the LinkedIn archive (see [`archive-files.md`](archive-files.md)). The user corrects `profil.md` itself, never a generated CV or cover letter, so every later document stays consistent.
3. **Every value records its source.** This lets the agent detect contradictions when the archive changes (#24).
4. **Facts once, texts in two languages.** Names, dates, links and contact details are written once. Texts used in documents have a French and an English version. The agent picks the version that matches the language of the job offer.
5. **Labels in the interface language.** Section titles, field labels and the "About this file" text are written in the interface language chosen at onboarding (`interface_language`, see [`onboarding.md`](onboarding.md)). Code never relies on a label: every field has a fixed internal key, mapped to its label in each language. Only French labels exist for now; English labels are tracked in #55.
6. **No real data in the repository.** The real `profil.md` is never committed. This document only contains a fictional example.

## File layout

1. **Front matter** (YAML, between two `---` lines). It must be the very first thing in the file.
2. **"About this file" text**, in the interface language, explaining how to use the file.
3. **Sections 1 to 13**, in the order below.

## Front matter

| Field | Example | Meaning |
| --- | --- | --- |
| `schema_version` | `1` | Version of this structure, so future versions of the tool can migrate older files |
| `interface_language` | `fr` | Language of the labels and of everything the user reads: `fr` or `en`. Chosen at onboarding, `fr` by default. |
| `archive_date` | `2026-11-16` | Export date of the LinkedIn archive used |
| `generated_on` | `2026-11-20` | Date the agent generated the file |
| `reviewed` | `false` | Set to `true` by the user after the first review |

On the first run, the agent generates `profil.md` and stops. It generates no CV or cover letter while `reviewed` is `false` (see #16). On later runs, reviewing the file is optional.

## "About this file" text

This exact text follows the front matter (French version):

```markdown
> **À propos de ce fichier**
>
> `profil.md` est la **source unique** de toutes tes candidatures : chaque CV et chaque lettre de motivation est généré à partir de ce fichier. Pour corriger une information (email, intitulé de poste, compétence…), corrige-la **ici**, jamais dans un CV ou une lettre déjà générés : la correction s'appliquera à tous les documents suivants.
>
> **Ce qu'il faut faire**
> - Remplace chaque `[À COMPLÉTER]` : aucun CV n'est généré tant qu'il en reste un.
> - Tu ne veux pas afficher une information (téléphone, projets…) ? Remplace sa valeur par `[NE PAS AFFICHER]` : elle n'apparaîtra sur aucun document. Seuls ton prénom, ton nom et au moins un moyen de contact (email, téléphone ou LinkedIn) sont obligatoires.
> - Relis les textes en français **et** en anglais.
> - Tes expériences et tes projets sont dans `experiences.md` et `projets.md` : relis-les aussi.
> - Quand tout est bon, passe `reviewed: false` à `reviewed: true`, tout en haut du fichier.
>
> **Les commentaires `<!-- src: ... -->`**
> Ils sont invisibles dans l'aperçu du fichier et indiquent d'où vient chaque information :
> - `src: linkedin` : lue dans ton archive LinkedIn (le nom du fichier source est précisé) ;
> - `src: user` : saisie par toi ;
> - `src: ai` : texte rédigé ou traduit par l'IA, à relire avec attention.
>
> Ils permettent à l'agent de savoir d'où vient chaque valeur, et de te signaler une contradiction quand ton archive LinkedIn change. **Ne les supprime pas.** Tu n'as pas besoin de les modifier quand tu corriges une valeur : l'agent repère lui-même tes changements en comparant avec l'archive.
```

## Source comments

Each value is followed by an HTML comment giving its source. HTML comments are hidden when Markdown is rendered, but the agent reads them.

| Comment | Meaning |
| --- | --- |
| `<!-- src: linkedin, Positions.csv -->` | Read from the LinkedIn archive. The source file is named. |
| `<!-- src: user -->` | Written by the user, or a value the archive does not contain |
| `<!-- src: ai -->` | Written, condensed or translated by the AI. The user must review it. |

- For a single value, the comment is placed at the end of the line.
- For a block of text, the comment is placed at the end of the line that introduces the block.
- For a table row, the comment is placed inside the last cell, so the table still renders correctly.
- The user never has to edit these comments. The agent detects user changes by comparing values with the archive (#24).

## Placeholders and the required minimum

| Value | Meaning | Agent behaviour |
| --- | --- | --- |
| `[À COMPLÉTER]` | Not answered yet | Generates no CV or cover letter while one remains |
| `[NE PAS AFFICHER]` | The user chose not to show it | Leaves the value out of every document, and keeps this choice when the archive changes |
| `aucun` | Optional field with nothing to say (for example no long-term ambition) | Never blocks generation. Written when an optional onboarding question is skipped. |

- **Required minimum:** first name, last name, and at least one contact method among email, phone and LinkedIn. If all three contact methods are hidden, the agent explains why it cannot generate a CV.
- Every other value is optional.
- A section with no entry is left out of the CV.
- A deleted line is not a valid way to hide a value: the agent cannot tell a choice from an oversight, so it writes `[À COMPLÉTER]` again.

## Dates

Dates are written `YYYY-MM`. A current position or project has the end date `présent`. The agent converts the English month abbreviations of the archive, such as `Sep 2026`, into this format.

## Sections

### 1. Identité et contact

| Field | Source | Notes |
| --- | --- | --- |
| Prénom | `Profile.csv` | Required |
| Nom | `Profile.csv` | Required |
| Titre (FR) | ai | CV title, condensed from the LinkedIn headline |
| Titre (EN) | ai | Translation of the French title |
| Email | `Email Addresses.csv` | Primary address only |
| Téléphone | `PhoneNumbers.csv` | Duplicates removed |
| LinkedIn | user | Not in the archive |
| Portfolio | `Profile.csv` (Websites) | |
| GitHub | user | Not in the archive |

### 2. Recherche

All fields come from the user, through the onboarding questions (see [`onboarding.md`](onboarding.md)). They are used to score job offers. Only the CV location of the search zones is ever shown on a CV.

| Field | Format | Example |
| --- | --- | --- |
| Postes visés | 1 to 3 titles, by priority | Data Analyst, Analytics Engineer |
| Type de contrat | `CDI`, `CDD`, `freelance`, `alternance`, `stage` | CDI |
| Télétravail | `sur site`, `hybride`, `full remote`, `indifférent` | hybride |
| Disponibilité | `immédiate`, `préavis` | préavis |
| Ambition à long terme | Free text, or `aucun` | Data Engineer |
| Ce que je ne veux pas | Free text, or `aucun` | Postes sans stack technique moderne |

#### Zones de recherche

A table with one row per zone, 5 at most. The first row is pre-filled from `Profile.csv` (Geo Location) and confirmed at onboarding.

| Column | Shown on a CV | Example |
| --- | --- | --- |
| Zone | No | Bordeaux et alentours |
| Localisation (CV) | Yes | Bordeaux (mobilité) |

- A CV shows the location of the zone that contains the job offer.
- An offer outside every zone is **flagged, never rejected**. Its CV shows the location of the first zone.

### 3. Positionnement

| Field | Source | Notes |
| --- | --- | --- |
| Résumé LinkedIn | `Profile.csv` (Summary) | Full text, in its original language. Source material only, never copied as is into a document. |
| Points forts (FR) | ai suggestion | What makes the profile stand out, used in cover letters. Reviewed and corrected by the user. |
| Points forts (EN) | ai | Translation |

### 4. Expériences

A reference only. Positions, with their dates, locations and bullet point banks, are stored in `experiences.md` (see [`experience-project-files.md`](experience-project-files.md)). The section contains this single line:

```markdown
Voir [`experiences.md`](experiences.md).
```

### 5. Formation

| Field | Source | Notes |
| --- | --- | --- |
| École, Diplôme | `Education.csv` | |
| Domaine | user | Not in the archive |
| Début, Fin | `Education.csv` | Often missing in the archive |
| Détails | `Education.csv` (Notes, Activities) | Optional |

### 6. Compétences

A table with one row per skill.

| Column | Source | Notes |
| --- | --- | --- |
| Compétence | `Skills.csv` | Near-duplicates are merged by the AI and confirmed by the user |
| Catégorie | ai suggestion | For example Langages, Bases de données, Cloud |
| Mise en avant | `Skills.csv` order, then user | `oui` or `non`. The first rows of `Skills.csv` may be the profile's top skills (open question in `archive-files.md`). |

**Safety rule:** a CV never shows a skill that is not in this section.

Skill levels are deliberately not recorded: they are never shown on a CV, and asking for one level per skill would make onboarding too long when the archive lists many skills.

### 7. Certifications

Nom, Organisme, Date, Lien, from `Certifications.csv`. A CV shows them as one line at the end of the skills section (see [`editable-areas.md`](editable-areas.md)).

### 8. Projets

A reference only. Projects, with their links, stacks and summaries, are stored in `projets.md` (see [`experience-project-files.md`](experience-project-files.md)). The section contains this single line:

```markdown
Voir [`projets.md`](projets.md).
```

### 9. Langues

Langue and Niveau, from `Languages.csv`.

### 10. Bénévolat

Organisme, Rôle, Cause, Début, Fin, Description, from `Volunteering.csv`. A CV can show volunteering as a miscellaneous line of the "Langues & divers" section (see [`editable-areas.md`](editable-areas.md)).

### 11. Références

| Field | Source | Notes |
| --- | --- | --- |
| Références sur demande | `Recommendations_Received.csv` (Status) | `oui` if at least one recommendation is `VISIBLE`. If `oui`, the CV ends with "Références disponibles sur demande" or "References available on request". Never mentioned in a cover letter. |

### 12. Style d'écriture

Optional. Left out when the user answered `aucun` to the style question. How the sources are selected and used is defined in [`onboarding.md`](onboarding.md#writing-style).

| Field | Source | Notes |
| --- | --- | --- |
| Sources | user | `posts`, `lettres` or `les deux` |
| Portrait | ai | Short description of the user's style: tone, sentence length, recurring words, structure of a letter. Reviewed by the user. Style only, never content. |

### 13. Divers

Optional. Items the LinkedIn archive does not contain, given by the user through an optional onboarding question (see [`onboarding.md`](onboarding.md)). Written `aucun` when the user skips the question. A CV can show them as miscellaneous lines of the "Langues & divers" section, as defined in [`editable-areas.md`](editable-areas.md).

A table with one row per item.

| Column | Source | Notes |
| --- | --- | --- |
| Type | user | `open source`, `concours` or `centre d'intérêt` |
| Texte (FR) | user | One short line, for example `Contributions à pandas (documentation)` or `Alpinisme et randonnée` |
| Texte (EN) | ai | Translation, reviewed by the user |

The no-invention rule of [`experience-project-files.md`](experience-project-files.md) applies: the agent translates these lines but never adds an item or a detail.

## Replaced files

`profil.md`, `experiences.md` and `projets.md` replace the three profile files of the current workflow:

| Current file | Content | New location |
| --- | --- | --- |
| `competences.txt` | Identity, search, stack, experiences, projects, positioning | `profil.md` sections 1 to 3 and 6, `experiences.md`, `projets.md` |
| `skills_completes.txt` | Full skill list with levels, soft skills, safety rule | `profil.md` section 6 and its safety rule. Levels are not kept. |
| `projets_portfolio.txt` | Projects in French and English | `projets.md` |

These files contradict each other and the LinkedIn archive on several values, such as the contact email or the number of learners coached. Writing each piece of information in one place only removes this risk.

## Fictional example

An extract of a generated `profil.md`. The person and all values are fictional.

```markdown
---
schema_version: 1
interface_language: fr
archive_date: 2026-11-16
generated_on: 2026-11-20
reviewed: false
---

> **À propos de ce fichier**
> (texte complet défini plus haut)

## 1. Identité et contact

- Prénom : Camille <!-- src: linkedin, Profile.csv -->
- Nom : Martin <!-- src: linkedin, Profile.csv -->
- Titre (FR) : Data Analyst | SQL · Python · Power BI <!-- src: ai -->
- Titre (EN) : Data Analyst | SQL · Python · Power BI <!-- src: ai -->
- Email : camille.martin@example.com <!-- src: linkedin, Email Addresses.csv -->
- Téléphone : [NE PAS AFFICHER] <!-- src: user -->
- LinkedIn : [À COMPLÉTER] <!-- src: user -->
- Portfolio : https://example.com/camille <!-- src: linkedin, Profile.csv -->
- GitHub : [À COMPLÉTER] <!-- src: user -->

## 2. Recherche

- Postes visés : Data Analyst, Analytics Engineer <!-- src: user -->
- Type de contrat : CDI <!-- src: user -->
- Télétravail : hybride <!-- src: user -->
- Disponibilité : [À COMPLÉTER] <!-- src: user -->
- Ambition à long terme : aucun <!-- src: user -->
- Ce que je ne veux pas : aucun <!-- src: user -->

### Zones de recherche

| Zone | Localisation (CV) |
| --- | --- |
| Lyon et alentours | Lyon <!-- src: user --> |

## 4. Expériences

Voir [`experiences.md`](experiences.md).

## 6. Compétences

| Compétence | Catégorie | Mise en avant |
| --- | --- | --- |
| SQL | Langages | oui <!-- src: linkedin, Skills.csv --> |
| Power BI | Visualisation | oui <!-- src: linkedin, Skills.csv --> |

## 11. Références

- Références sur demande : oui <!-- src: linkedin, Recommendations_Received.csv -->

## 13. Divers

| Type | Texte (FR) | Texte (EN) |
| --- | --- | --- |
| concours | Advent of Code 2025, 30 étoiles | Advent of Code 2025, 30 stars <!-- src: ai --> |
| centre d'intérêt | Escalade et randonnée | Climbing and hiking <!-- src: ai --> |
```
