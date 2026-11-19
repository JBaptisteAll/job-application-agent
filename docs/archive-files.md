# LinkedIn archive files

> Status: phase 1 specification. Related issues: #15 (this document), #16 (onboarding), #44 (contacts feature), #50 (differences between exports).

This document defines which files and columns of the LinkedIn data export the agent may read, how it finds them, and what it does when one is missing. Any file or column not listed here is ignored by design.

## Principles

1. **Allowlist only.** The agent reads only the files listed below. Any other file, including new files added by LinkedIn in future exports, is ignored automatically.
2. **Only useful columns.** In an allowed file, the agent reads only the columns needed for the CV, the cover letter or an optional feature.
3. **Every file is optional.** LinkedIn adds, removes and renames files between exports (see #50). A missing file never stops the agent.
4. **Filter in code before any AI call.** Files are parsed and filtered by code. Only the data needed for a task is sent to the AI model, to reduce cost and noise.
5. **A human always decides.** The agent prepares documents and drafts. It never sends a message or submits an application by itself.

These choices are made for usefulness, cost and reliability. The user processes their own export for their own job search, which is a personal use.

## Data sources

- **The LinkedIn data export** (`Complete_LinkedInDataExport_<MM-DD-YYYY>.zip`) is the only data source.
- **The profile PDF** downloaded from LinkedIn is not read by the agent. It is used only as a reference in tests (#31). Comparing it with the export showed two gaps, the LinkedIn profile URL and the field of study, which the user fills in `profil.md`.

## Allowed files and columns

| File | Columns read | Used for |
| --- | --- | --- |
| `Profile.csv` | First Name, Last Name, Headline, Summary, Geo Location, Websites | Name, headline, summary, city, portfolio link |
| `Email Addresses.csv` | Email Address, Primary | Contact email: the primary address only |
| `PhoneNumbers.csv` | Number, Type | Contact phone number |
| `Positions.csv` | Company Name, Title, Description, Location, Started On, Finished On | Experience |
| `Education.csv` | School Name, Start Date, End Date, Notes, Degree Name, Activities | Education |
| `Skills.csv` | Name | Skills, in file order (see open questions) |
| `Certifications.csv` | Name, Url, Authority, Started On, Finished On | Certifications |
| `Projects.csv` | Title, Description, Url, Started On, Finished On | Projects section |
| `Languages.csv` | Name, Proficiency | Languages |
| `Volunteering.csv` | Company Name, Role, Cause, Started On, Finished On, Description | Volunteering |
| `Recommendations_Received.csv` | Status | Recommendations rule below |

**Recommendations rule:** if at least one recommendation has the status `VISIBLE`, the CV ends with "References available on request". The names and text of recommendations are never read, and recommendations are never mentioned in the cover letter.

### File used only by an optional feature

| File | Columns read | Used for |
| --- | --- | --- |
| `Connections.csv` | All | Contacts feature (#44) |

- This file is read **only** by the contacts feature, never during profile generation.
- Code filters connections by the target company before any AI call.
- Messages are drafted only. The user always sends them manually, since LinkedIn's terms forbid automated messaging.
- The file starts with a few lines of notes before the header row. The parser skips them.

### Pending decision

The `Jobs/` folder, including `Job Seeker Preferences.csv`, was present in the 2026-08-30 export and absent from the 2026-11-16 export. Its status will be decided once #50 confirms why.

## Excluded columns in allowed files

| File | Excluded columns | Reason |
| --- | --- | --- |
| `Profile.csv` | Maiden Name, Address, Birth Date, Zip Code, Industry, Twitter Handles, Instant Messengers | Not useful for a CV or cover letter. A French CV shows the city only. |
| `Email Addresses.csv` | Confirmed, Updated On | Not needed |
| `PhoneNumbers.csv` | Extension | Not needed |
| `Certifications.csv` | License Number | Not needed, and sometimes a copy of the URL |
| `Recommendations_Received.csv` | All except Status | See the recommendations rule |

## Files never read

Any file that is not listed above is ignored. This includes private files such as `messages.csv`, the other message files, `SearchQueries.csv`, `Logins.csv`, `Security Challenges.csv`, `Private_identity_asset.csv` and the advertising files.

Two files were reviewed and deliberately left out:

- `Profile Summary.csv`: empty in both exports reviewed; the `Summary` column of `Profile.csv` holds the summary.
- `Endorsement_Received_Info.csv`: every skill was endorsed once, often under a name that differs from `Skills.csv`, so it adds no useful signal.

## File name matching

- Names are compared **without regard to letter case**.
- An optional suffix made of an underscore and digits before `.csv` is accepted, because older exports used names such as `Comments_<member_id>.csv`.
- Files are searched at the root of the archive. Subfolders are only used for files explicitly listed with their folder.

## Missing files and missing values

- **Required sections**: identity, contact details, experience, education, skills and languages. If their file or value is missing, `profil.md` shows `[À COMPLÉTER]`.
- **Optional sections**: certifications, projects, volunteering and the recommendations rule. If their file is missing, the section is left out.
- The agent refuses to generate a CV while `profil.md` still contains `[À COMPLÉTER]` (see #16).

## Known data quality issues

Found in real exports. The archive parser (#21) must handle them:

- Line breaks are removed from long texts, so section titles are glued to the next sentence.
- HTML entities remain in text, such as `&amp;` instead of `&`.
- `Websites` uses a special format: `[LABEL:https://...]`.
- Values may have extra spaces at the end or double spaces inside.
- Dates use English month abbreviations, such as `Sep 2026`. An empty end date means "present".
- Some dates are missing, for example education dates.
- The same phone number can appear several times in different formats, with empty rows.
- `Skills.csv` contains near-duplicates, such as `Python` and `Python (langage de programmation)`, in several languages.
- Project titles can contain emojis, and project URLs can be empty.

## Open questions

- **Skills order:** in the export reviewed, the first three rows of `Skills.csv` match the "Top skills" shown on the profile PDF. This must be confirmed on another export before the agent relies on it.
- **`Jobs/` folder:** see the pending decision above and #50.
