# Experience and project files

> Status: phase 1 specification. Related issues: #57 (this document), #14 (`profil.md` structure), #16 (onboarding), #17 (editable areas), #24 (contradictions), #58 (GitHub repositories).

Experiences and projects are stored in two dedicated files, `experiences.md` and `projets.md`, next to `profil.md`. The agent builds them once, at onboarding, with more content than a single CV needs. Each later application only selects, orders and adapts this content, so every CV comes from the same reviewed base. This document defines the layout and fields of both files, their identifiers, and the rule that keeps enriched texts true.

## Principles

1. **Built once, selected many times.** Onboarding writes rich content: a bank of bullet points for each experience, a full summary for each project. For each job offer, the agent picks the most relevant content. What it may change on a CV is defined in #17.
2. **Each piece of information in one place.** Company names, job titles, locations and dates of positions are written only in `experiences.md`. Project names, links and dates are written only in `projets.md`. `profil.md` only points to these files (see [`profil-structure.md`](profil-structure.md)).
3. **Enriched, never invented.** The agent may rewrite and highlight, but every fact comes from the archive or from the user (see [No-invention rule](#no-invention-rule)).
4. **Reviewed before use.** No CV or cover letter is generated while one of the three files still has `reviewed: false`.
5. **Same conventions as `profil.md`.** Front matter, "About this file" text, `<!-- src: ... -->` comments, placeholders, `YYYY-MM` dates, labels in the interface language with fixed internal keys, French and English texts. Everything defined in [`profil-structure.md`](profil-structure.md) applies here unless this document says otherwise.
6. **No real data in the repository.** Like `profil.md`, the real files are never committed. This document only contains fictional examples.

## Front matter

Both files use the same front matter as `profil.md`: `schema_version`, `interface_language`, `archive_date`, `generated_on` and `reviewed`. The agent keeps `interface_language` identical in the three files.

## "About this file" text

This text follows the front matter of `experiences.md` (French version). `projets.md` uses the same text, with « tes projets » instead of « tes expériences » and « le résumé » instead of « les points ».

```markdown
> **À propos de ce fichier**
>
> Ce fichier contient **toutes tes expériences**, rédigées une fois pour toutes. Pour chaque offre, l'agent choisit les points les plus adaptés : un CV n'en affiche que 2 ou 3 par expérience. Pour corriger une information, corrige-la **ici**, jamais dans un CV déjà généré.
>
> **Ce qu'il faut faire**
> - Relis chaque point en français **et** en anglais. Tu peux en modifier, en supprimer ou en ajouter.
> - Remplace chaque `[CHIFFRE ?]` par le vrai chiffre, ou reformule le point sans chiffre : aucun CV n'est généré tant qu'il en reste un.
> - Tu ne veux pas afficher une expérience ? Passe `Afficher : oui` à `Afficher : non`. Ne la supprime pas.
> - Ne modifie jamais les identifiants (`exemple-sa-2024-03`, `b1`…) : l'agent s'en sert pour retrouver chaque point.
> - Quand tout est bon, passe `reviewed: false` à `reviewed: true`, tout en haut du fichier.
>
> Les commentaires `<!-- src: ... -->` fonctionnent comme dans `profil.md`. **Ne les supprime pas.**
```

## Identifiers

Every experience, project and bullet point has an identifier. CV generation and tests (#17) refer to content by identifier, never by position in the file.

| Content | Format | Example |
| --- | --- | --- |
| Experience | Company and start date | `exemple-sa-2024-03` |
| Project | Project name | `suivi-ventes` |
| Bullet point | Experience identifier, then `b` and a number | `exemple-sa-2024-03.b2` |

- An identifier is lowercase, uses only `a-z`, `0-9` and hyphens, with accents, emojis and punctuation removed.
- It is created once and **never changes**, even when the user renames a project or edits a job title. A new archive with a new position adds a new identifier without shifting the others.
- If two entries would get the same identifier, the second one ends with `-2`.
- When #58 is implemented, a project linked to a GitHub repository uses the repository name as its identifier.
- Bullet numbers are never reused: if the user deletes `b3`, the next bullet added is `b7`, not `b3`.

## `experiences.md`

One entry per position from `Positions.csv`, most recent first. Each entry starts with a level-3 heading that contains its identifier and the company name, for example `### exemple-sa-2024-03 : Exemple SA`.

| Field | Source | Notes |
| --- | --- | --- |
| Entreprise | `Positions.csv` | In the heading, written once |
| Poste (FR) / Poste (EN) | `Positions.csv`, then ai | The archive language is kept, the other version is a translation |
| Lieu (FR) / Lieu (EN) | `Positions.csv`, then ai | For example `Miami, États-Unis` / `Miami, USA` |
| Début, Fin | `Positions.csv` | `YYYY-MM` or `présent` |
| Afficher | user | `oui` by default. `non` hides the position from every document without deleting it. |
| Texte complet | `Positions.csv` (Description) | Original language. Source material for bullet points and cover letters, never copied as is into a document. |
| Banque de points | ai, reviewed by the user | 3 to 8 bullet points, see below |

### Bullet point bank

- **3 to 8 bullet points per position**, depending on how much the full text contains. The agent never adds points to reach a number: a short, old position gets 3, a rich, recent one up to 8.
- At least 3 points give the agent a real choice when a CV shows 2 or 3 of them.
- Each point is written in French **and** English under the same identifier. Selecting `b2` for an offer gives the same content in a French or an English CV, and the user can check each translation line by line.
- Points are written for a CV: one line, an action verb first, the most concrete fact available.
- The user can edit, delete or add points. A point written by the user gets `<!-- src: user -->`.
- If the full text is empty, the agent writes no points and adds `[À COMPLÉTER]` in the bank, so the user can describe the position.

## `projets.md`

One entry per project from `Projects.csv`. Each entry starts with a level-3 heading that contains its identifier and the project name in the interface language, for example `### suivi-ventes : Suivi des ventes`.

| Field | Source | Notes |
| --- | --- | --- |
| Nom (FR) / Nom (EN) | `Projects.csv` (Title), then ai | Emojis removed. A proper name can stay the same in both languages. |
| Début, Fin | `Projects.csv` | `YYYY-MM` or `présent`. Optional, often missing in the archive. |
| Lien | `Projects.csv` (Url) | Often empty in the archive. Filled from GitHub when #58 is implemented. |
| Stack | ai suggestion | Main tools, for example `Python · dbt · GitHub Actions` |
| Afficher | user | `oui` by default, same as for experiences |
| Texte complet | `Projects.csv` (Description) | Original language, source material |
| Résumé (FR) / Résumé (EN) | ai, reviewed by the user | Full summary, see below |

### Project summary

- **120 to 150 words per language.** It covers the business problem, the solution, the stack and the result.
- This length is a target, not an obligation. When the full text is too short, the agent writes a shorter summary and says so, rather than filling it. The user can complete it.
- The summary is not shown on a CV as is. For each offer, the agent writes a 2 or 3 line synthesis from it, under the rules of #17.
- **Stack safety rule:** the stack only lists skills present in section 6 of `profil.md`. A tool found in the full text but missing from section 6 is flagged to the user, who decides whether to add it to section 6.

## No-invention rule

This rule applies to every text the AI writes in both files: bullet points, project summaries, translations.

**The agent may:**

- rewrite, structure and highlight;
- use CV vocabulary, such as action verbs and the usual terms of the field;
- translate between French and English.

**The agent never:**

- adds a fact that is neither in the archive nor in a user answer: a tool, a figure, a result, a responsibility, a team size;
- estimates a figure. When a figure would make a point stronger but is missing, it writes `[CHIFFRE ?]` in the point;
- inflates a role: "took part in" never becomes "led";
- uses a skill missing from section 6 of `profil.md`.

Example, from the archive text *"Création de tableaux de bord pour les équipes commerciales"*:

| Bullet point | Verdict |
| --- | --- |
| Conception de tableaux de bord de suivi commercial pour les équipes de vente | Allowed: rewording |
| Conception de tableaux de bord pour `[CHIFFRE ?]` équipes commerciales | Allowed: the figure is asked, not invented |
| Conception de 12 tableaux de bord Power BI utilisés par 50 commerciaux | Forbidden: figures and tool invented |

### Placeholders

These files add one placeholder to those of [`profil-structure.md`](profil-structure.md#placeholders-and-the-required-minimum):

| Value | Meaning | Agent behaviour |
| --- | --- | --- |
| `[CHIFFRE ?]` | A figure the agent could not find | Generates no CV while one remains. The user replaces it with the real figure, or rewrites the point without it. |

## Later runs

- A new position or project in a new archive adds a new entry, with its own identifier and `reviewed` set back to `false` in the file concerned.
- The agent never overwrites a point, a summary or a value written or corrected by the user. When the archive text of an existing entry changes, it flags the difference instead (#24).

## Fictional examples

The person and all values are fictional.

### `experiences.md`

```markdown
---
schema_version: 1
interface_language: fr
archive_date: 2026-11-16
generated_on: 2026-11-21
reviewed: false
---

> **À propos de ce fichier**
> (texte complet défini plus haut)

### exemple-sa-2024-03 : Exemple SA

- Poste (FR) : Analyste de données <!-- src: linkedin, Positions.csv -->
- Poste (EN) : Data Analyst <!-- src: ai -->
- Lieu (FR) : Lyon, France <!-- src: linkedin, Positions.csv -->
- Lieu (EN) : Lyon, France <!-- src: ai -->
- Début : 2024-03 <!-- src: linkedin, Positions.csv -->
- Fin : présent <!-- src: linkedin, Positions.csv -->
- Afficher : oui <!-- src: user -->

**Texte complet** <!-- src: linkedin, Positions.csv -->
Analyse des ventes pour trois équipes commerciales, création de tableaux de bord et automatisation du reporting hebdomadaire en Python.

**Banque de points** <!-- src: ai -->
- `b1` FR : Conception de tableaux de bord de suivi commercial pour 3 équipes de vente
- `b1` EN : Designed sales monitoring dashboards for 3 sales teams
- `b2` FR : Automatisation du reporting hebdomadaire en Python
- `b2` EN : Automated the weekly reporting in Python
- `b3` FR : Analyse des ventes pour orienter les priorités commerciales, réduisant le reporting manuel de `[CHIFFRE ?]` heures par semaine
- `b3` EN : Analysed sales to guide commercial priorities, cutting manual reporting by `[CHIFFRE ?]` hours a week
```

### `projets.md`

```markdown
---
schema_version: 1
interface_language: fr
archive_date: 2026-11-16
generated_on: 2026-11-21
reviewed: false
---

> **À propos de ce fichier**
> (texte complet défini plus haut)

### suivi-ventes : Suivi des ventes

- Nom (FR) : Suivi des ventes <!-- src: ai -->
- Nom (EN) : Sales Tracker <!-- src: linkedin, Projects.csv -->
- Début : 2025-01 <!-- src: linkedin, Projects.csv -->
- Fin : 2025-03 <!-- src: linkedin, Projects.csv -->
- Lien : [NE PAS AFFICHER] <!-- src: user -->
- Stack : Python · SQL · Power BI <!-- src: ai -->
- Afficher : oui <!-- src: user -->

**Texte complet** <!-- src: linkedin, Projects.csv -->
Sales tracking project built during a bootcamp...

**Résumé (FR)** <!-- src: ai -->
(120 à 150 mots : problème métier, solution, stack, résultat)

**Résumé (EN)** <!-- src: ai -->
(120 to 150 words: business problem, solution, stack, result)
```
