# Editable areas of the CV and cover letter

> Status: phase 1 specification, updated in phase 2. Related issues: #17 (this document), #14 (`profil.md` structure), #16 (onboarding), #18 (CV template), #57 (experience and project files).

This document defines what the agent may change in the CV and the cover letter for each job offer, and what always stays untouched. It is the main safeguard against invented content: every rule below can be checked automatically.

## Principles

1. **Fixed templates.** The CV and the cover letter are built from fixed templates. The agent never changes the layout, the fonts or the order of the sections.
2. **Three levels of freedom.** Every area is either copied, selected or written (see [Levels](#levels)).
3. **No invention.** The no-invention rule of [`experience-project-files.md`](experience-project-files.md) applies to every written area of both documents: each tool, figure or result must come from `profil.md`, `experiences.md` or `projets.md`.
4. **Files are corrected, never documents.** A wrong value is corrected in the source files, as defined in [`profil-structure.md`](profil-structure.md). The agent never fixes a fact directly in a generated document.
5. **Consistent documents.** The CV and the cover letter of an application always show the same title, the same location and the same contact details.
6. **A human always decides.** The agent never blocks on a judgment call. It flags it in the generation summary, and the user decides (see [Generation summary](#generation-summary)).

## Levels

| Level | What the agent does | How it is checked |
| --- | --- | --- |
| Copied | Copies the value from the source files, unchanged | The text in the document is identical to the source |
| Selected | Chooses and orders existing items, without writing anything | Every item in the document has an identifier or a value that exists in the source files |
| Written | Writes a text, within the rules of its area | Every tool, figure and result in the text exists in the source files |

## CV

### Copied areas

| Area | Source | Rule |
| --- | --- | --- |
| Name and contact details | `profil.md`, section 1 | Phone, email, city, LinkedIn, GitHub and portfolio, on a single line. Links are shown as short clickable labels (`LinkedIn`, `GitHub`, `Portfolio`), not as full addresses. A hidden value is not shown, with its separator. |
| Company, job title, location and dates of each experience | `experiences.md` | Copied in the language of the offer |
| Education | `profil.md` | Copied unchanged |
| Certifications | `profil.md`, section 7 | One line at the end of the skills section: "Certifications: name, name". Not shown if there is none. |
| Languages | `profil.md`, section 9 | First line of the "Langues & divers" section |
| "References available on request" | `profil.md`, section 11 | Shown only if the value is `oui`, as defined in `profil-structure.md` |
| Layout | CV template | Never changed |

### Selected areas

| Area | Source | Rule |
| --- | --- | --- |
| Displayed location | Search zones from the onboarding (#16) | The zone that matches the offer. If the offer matches no zone, the agent uses the first zone and flags the offer as out of scope. |
| Skills | `profil.md`, section 6 | The agent filters and reorders the skills, starting with those named in the offer. It never adds a skill and never renames one. |
| Experience bullet points | `experiences.md` | 0 to 3 points per position, chosen by identifier: 2 or 3 for relevant positions, 0 or 1 for old positions or positions unrelated to the offer. Experiences stay in reverse chronological order. |
| Projects | `projets.md` | The agent chooses and orders the projects that best match the offer. At least two projects are shown when two or more exist. |
| Miscellaneous lines | `profil.md`, sections 10 and 13 | Up to two lines below the languages, chosen among volunteering, open source contributions, coding competitions and interests (see [Page fit](#page-fit)). |
| Hidden items | `experiences.md`, `projets.md` | An experience or a project with `Afficher: non` never appears. |
| Oldest experience | `experiences.md` | May be removed in favour of a project (see [Removing the oldest experience](#removing-the-oldest-experience)). |

### Written areas

| Area | Source | Rule |
| --- | --- | --- |
| CV title | Job offer | The exact title of the offer, word for word, so that ATS filters match it. If the title contains a seniority level (Senior, Lead, Confirmé…) or matches no target role in `profil.md`, the agent flags it. |
| Profile paragraph | `profil.md`, `experiences.md`, `projets.md` | At most 5 lines in the template. Uses the keywords of the offer and highlights the most relevant experience and skills. Facts only from the source files. |
| Project synthesis | `projets.md` | 2 to 4 lines written from the 120 to 150 word summary: 2 or 3 lines by default, up to 4 when space remains (see [Page fit](#page-fit)). |
| Experience bullet points | `experiences.md` | Small adjustments only (see below). |

### Small adjustments

The agent may adjust a selected bullet point to match the offer, within these limits.

**Allowed:**

- Replace a word with the term used in the offer, when the meaning is identical. For example, "tableaux de bord" becomes "dashboards".
- Move a keyword to the start of the point.
- Shorten a point to save space.

**Forbidden:**

- Add a tool, a figure or a result.
- Change a figure.
- Make a verb stronger. For example, "participated in" never becomes "led".
- Merge two points into a new claim.

**Check:** every tool and every figure in an adjusted point is present in the original point.

### Page fit

The CV always fits on one page. The agent fills the page in this order of priority:

1. Relevant experiences with 2 or 3 bullet points each.
2. At least two projects, when two or more exist.
3. Old or unrelated experiences, with 0 or 1 bullet point each. With 0 points, only the line with the job title, company and dates is shown, so the timeline has no gap.
4. If space remains: longer project syntheses (up to 4 lines, starting with the most relevant project), then more projects.
5. If space remains: up to two miscellaneous lines in "Langues & divers". Lines related to the offer come first (open source, coding competitions, data volunteering), then the others, such as interests.

If the CV still does not fit, the agent removes the oldest experience as a last resort (see below).

### Removing the oldest experience

As a last resort, the agent may remove an experience to make room for a personal project that matches the offer better. To keep this choice predictable:

- Only the **oldest** shown experience can be removed. An experience in the middle of the timeline is never removed, so the CV has no gap.
- At most **one** experience is removed per CV.
- The removed experience must be less relevant to the offer than the project that replaces it.
- The removal is listed in the generation summary, so the user can restore the experience.

## Cover letter

### Copied areas

| Area | Source | Rule |
| --- | --- | --- |
| Sender header | `profil.md`, section 1 | Name, phone and email, with the same rules as the CV. A hidden value is not shown. |
| Salutation | Cover letter template | "Madame, Monsieur," or "Dear Hiring Manager," |
| Closing formula and signature | Cover letter template | Fixed by the template. The agent never writes its own closing formula. |
| Layout | Cover letter template | Never changed |

### Selected areas

| Area | Source | Rule |
| --- | --- | --- |
| Language | Job offer | French or English template, in the language of the offer |
| Location in the header | Displayed location of the CV | Always the same as the CV |
| City in the date line | Displayed location of the CV | If the displayed location is a country only, the date line shows the date alone. |

### Written areas

| Area | Source | Rule |
| --- | --- | --- |
| Recipient | Job offer | "À l'attention de l'équipe de recrutement de [company]", with the company name from the offer |
| Date | System date | The date of the day |
| Subject line | CV title | "Candidature au poste de [title]", with exactly the same title as the CV |
| Body | Source files, job offer, style portrait (#16) | See [Writing rules](#writing-rules) |

### Facts used in the cover letter

The cover letter is written after the CV. It cites only experiences and projects shown on the CV, but it may use all their content in the source files. This way, the letter adds something to the CV without repeating it, and everything it cites can be found on the CV.

| What the letter cites | Allowed | Reason |
| --- | --- | --- |
| A bullet point selected for the CV | Yes | The letter develops it |
| A bullet point not selected for the CV, for an experience shown on the CV | Yes | The recruiter finds the experience on the CV, and the letter adds a detail |
| Details from the full summary of a project shown on the CV | Yes | The CV synthesis has no room for them |
| A project not shown on the CV | No | If a project is strong enough for the letter, it belongs on the CV |
| An experience removed or hidden from the CV | No | If an experience is relevant enough for the letter, it belongs on the CV |

Recommendations are never mentioned in the cover letter, as defined in `profil-structure.md`.

### Writing rules

These rules apply to every user. They are universal formatting and quality rules.

- At most 3 body paragraphs and 500 words in total.
- At least one concrete fact per paragraph, such as a figure, a tool or a precise context, taken from the source files.
- At least one direct reference to the offer: the company, its sector or its technical stack.
- The keywords of the offer are reused.
- No bullet points, no bold and no italic in the body.
- No parentheses.
- No ellipsis, except in a quotation.

These rules apply to every written area of the CV and the cover letter:

- No em dash (`—`).
- No double spaces.

Forbidden phrases and style rules that make a letter sound less generic are user preferences, not universal rules. They are tracked in a separate backlog issue, as default rules that each user can edit.

## Generation order

The agent works in this order for each offer. The CV comes first because it is the main document: it is built from a full review of all experiences and projects, and the cover letter then draws only from its content.

1. Read the offer and set the language, the displayed location and the CV title.
2. Build the whole CV:
   1. select the skills, the bullet points and the projects;
   2. decide whether to remove the oldest experience;
   3. write the profile paragraph, the project syntheses and the small adjustments.
3. Write the cover letter from the experiences and projects shown on the CV.
4. Run the checks of this document.
5. Write the generation summary.

## Generation summary

The agent never blocks on a judgment call. It lists these cases in the generation summary, and the user decides what to do:

- The CV title contains a seniority level or matches no target role in `profil.md`.
- The offer matches none of the search zones.
- The oldest experience was removed in favour of a project, with both names.

A `[CHIFFRE ?]` placeholder is different: it blocks generation, as defined in `experience-project-files.md`.

## Checks

Every rule of this document can be tested automatically:

| Check | Applies to |
| --- | --- |
| The text is identical to the source | Copied areas |
| Every identifier exists in `experiences.md` or `projets.md` | Bullet points and projects |
| Every skill exists in `profil.md`, section 6 | Skills |
| No item with `Afficher: non` appears | Experiences and projects |
| Every tool and every figure exists in the source files | Written areas |
| Every tool and every figure of an adjusted point exists in the original point | Small adjustments |
| At most one experience is removed, and it is the oldest | Experiences |
| At least two projects are shown when two or more exist | Projects |
| At most two miscellaneous lines are shown | Langues & divers |
| The CV fits on one page after PDF export | CV |
| Every experience and every project cited in the letter is shown on the CV | Cover letter and CV |
| The CV title and the letter subject use the same title | CV and cover letter |
| The CV and the letter show the same location | CV and cover letter |
| At most 3 body paragraphs and 500 words | Cover letter |
| No forbidden character (em dash, double space, and in the letter, parentheses, ellipsis, bullet points) | Written areas |
