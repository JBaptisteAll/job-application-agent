# `profil.md` structure

> Status: phase 1 specification. Related issues: #14 (this document), #15 (archive files), #16 (onboarding), #24 (contradictions), #25 (condensed texts and translations).

`profil.md` is the single profile file of the user. Every later step reads it: CV, cover letter and offer scoring. This document defines its layout, its sections and fields, the source of each value, and how missing or hidden values are handled.

## Principles

1. **Single source of truth.** `profil.md` replaces the three files of the current workflow (see [Replaced files](#replaced-files)). Every fact is written once.
2. **Pre-filled, then corrected by the user.** The agent fills everything it can from the LinkedIn archive (see [`archive-files.md`](archive-files.md)). The user corrects `profil.md` itself, never a generated CV or cover letter, so every later document stays consistent.
3. **Every value records its source.** This lets the agent detect contradictions when the archive changes (#24).
4. **Facts once, texts in two languages.** Names, dates, links and contact details are written once. Texts used in documents have a French and an English version. The agent picks the version that matches the language of the job offer.
5. **French labels.** Section titles and field labels are in French, since the tool targets the French job market for now.
6. **No real data in the repository.** The real `profil.md` is never committed. This document only contains a fictional example.

## File layout

1. **Front matter** (YAML, between two `---` lines). It must be the very first thing in the file.
2. **"About this file" text**, in French, explaining how to use the file.
3. **Sections 1 to 11**, in the order below.

## Front matter

| Field | Example | Meaning |
| --- | --- | --- |
| `schema_version` | `1` | Version of this structure, so future versions of the tool can migrate older files |
| `archive_date` | `2026-11-16` | Export date of the LinkedIn archive used |
| `generated_on` | `2026-11-20` | Date the agent generated the file |
| `reviewed` | `false` | Set to `true` by the user after the first review |

On the first run, the agent generates `profil.md` and stops. It generates no CV or cover letter while `reviewed` is `false` (see #16). On later runs, reviewing the file is optional.

## "About this file" text

This exact text follows the front matter:

```markdown
> **À propos de ce fichier**
>
> `profil.md` est la **source unique** de toutes tes candidatures : chaque CV et chaque lettre de motivation est généré à partir de ce fichier. Pour corriger une information (email, intitulé de poste, compétence…), corrige-la **ici**, jamais dans un CV ou une lettre déjà générés : la correction s'appliquera à tous les documents suivants.
>
> **Ce qu'il faut faire**
> - Remplace chaque `[À COMPLÉTER]` : aucun CV n'est généré tant qu'il en reste un.
> - Tu ne veux pas afficher une information (téléphone, projets…) ? Remplace sa valeur par `[NE PAS AFFICHER]` : elle n'apparaîtra sur aucun document. Seuls ton prénom, ton nom et au moins un moyen de contact (email, téléphone ou LinkedIn) sont obligatoires.
> - Relis les textes en français **et** en anglais.
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
| Ville | `Profile.csv` (Geo Location) | |
| Email | `Email Addresses.csv` | Primary address only |
| Téléphone | `PhoneNumbers.csv` | Duplicates removed |
| LinkedIn | user | Not in the archive |
| Portfolio | `Profile.csv` (Websites) | |
| GitHub | user | Not in the archive |

### 2. Recherche

All fields come from the user. They are used to score job offers and are never shown on a CV.

| Field | Example |
| --- | --- |
| Postes visés | Data Analyst, Analytics Engineer |
| Type de contrat | CDI |
| Zone géographique | Lyon et alentours |
| Télétravail | Hybride, 2 jours par semaine |
| Disponibilité | Immédiate |
| Ambition à long terme | Data Engineer |
| Ce que je ne veux pas | Postes sans stack technique moderne |

### 3. Positionnement

| Field | Source | Notes |
| --- | --- | --- |
| Résumé LinkedIn | `Profile.csv` (Summary) | Full text, in its original language. Source material only, never copied as is into a document. |
| Points forts (FR) | user, or ai suggestion | What makes the profile stand out, used in cover letters |
| Points forts (EN) | ai | Translation |

### 4. Expériences

One entry per position, most recent first.

| Field | Source | Notes |
| --- | --- | --- |
| Entreprise, Poste, Lieu | `Positions.csv` | |
| Début, Fin | `Positions.csv` | `YYYY-MM` or `présent` |
| Texte complet | `Positions.csv` (Description) | Original language. Used as source material for cover letters. |
| Version CV (FR) | ai | Condensed bullet points for the CV |
| Version CV (EN) | ai | Translation |

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
| Niveau | user | `notions`, `intermédiaire` or `avancé` |
| Catégorie | ai suggestion | For example Langages, Bases de données, Cloud |
| Mise en avant | `Skills.csv` order, then user | `oui` or `non`. The first rows of `Skills.csv` may be the profile's top skills (open question in `archive-files.md`). |

**Safety rule:** a CV never shows a skill that is not in this section.

### 7. Certifications

Nom, Organisme, Date, Lien, from `Certifications.csv`.

### 8. Projets

| Field | Source | Notes |
| --- | --- | --- |
| Titre, Début, Fin, Lien | `Projects.csv` | The link is often empty in the archive |
| Stack | ai suggestion | Main tools, for example `Python · dbt · Airflow` |
| Texte complet | `Projects.csv` (Description) | Original language |
| Version CV (FR) | ai | One or two lines |
| Version CV (EN) | ai | Translation |

### 9. Langues

Langue and Niveau, from `Languages.csv`.

### 10. Bénévolat

Organisme, Rôle, Cause, Début, Fin, Description, from `Volunteering.csv`.

### 11. Références

| Field | Source | Notes |
| --- | --- | --- |
| Références sur demande | `Recommendations_Received.csv` (Status) | `oui` if at least one recommendation is `VISIBLE`. If `oui`, the CV ends with "Références disponibles sur demande" or "References available on request". Never mentioned in a cover letter. |

## Replaced files

`profil.md` replaces the three profile files of the current workflow:

| Current file | Content | New location in `profil.md` |
| --- | --- | --- |
| `competences.txt` | Identity, search, stack, experiences, projects, positioning | Sections 1 to 4, 6 and 8 |
| `skills_completes.txt` | Full skill list with levels, soft skills, safety rule | Section 6 and its safety rule |
| `projets_portfolio.txt` | Projects in French and English | Section 8 |

These files contradict each other and the LinkedIn archive on several values, such as the contact email or the number of learners coached. A single file removes this risk.

## Fictional example

An extract of a generated `profil.md`. The person and all values are fictional.

```markdown
---
schema_version: 1
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
- Ville : Lyon, Auvergne-Rhône-Alpes, France <!-- src: linkedin, Profile.csv -->
- Email : camille.martin@example.com <!-- src: linkedin, Email Addresses.csv -->
- Téléphone : [NE PAS AFFICHER] <!-- src: user -->
- LinkedIn : [À COMPLÉTER] <!-- src: user -->
- Portfolio : https://example.com/camille <!-- src: linkedin, Profile.csv -->
- GitHub : [À COMPLÉTER] <!-- src: user -->

## 2. Recherche

- Postes visés : [À COMPLÉTER] <!-- src: user -->
- Type de contrat : [À COMPLÉTER] <!-- src: user -->

## 4. Expériences

### Data Analyst — Exemple SA

- Lieu : Lyon, France <!-- src: linkedin, Positions.csv -->
- Début : 2024-03 <!-- src: linkedin, Positions.csv -->
- Fin : présent <!-- src: linkedin, Positions.csv -->

**Texte complet** <!-- src: linkedin, Positions.csv -->
Analyse des ventes pour trois équipes commerciales, création de tableaux de bord et automatisation du reporting.

**Version CV (FR)** <!-- src: ai -->
- Création de tableaux de bord de suivi commercial pour 3 équipes
- Automatisation d'un reporting hebdomadaire en Python

**CV version (EN)** <!-- src: ai -->
- Built sales monitoring dashboards for 3 teams
- Automated a weekly report in Python

## 6. Compétences

| Compétence | Niveau | Catégorie | Mise en avant |
| --- | --- | --- | --- |
| SQL | [À COMPLÉTER] | Langages | oui <!-- src: linkedin, Skills.csv --> |
| Power BI | [À COMPLÉTER] | Visualisation | oui <!-- src: linkedin, Skills.csv --> |

## 11. Références

- Références sur demande : oui <!-- src: linkedin, Recommendations_Received.csv -->
```
