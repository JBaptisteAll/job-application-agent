# job-application-agent

**English** | [Français](README.fr.md)

Generates CVs and cover letters tailored to each job offer from a LinkedIn archive, with human review.

## Development setup

This repository uses [pre-commit](https://pre-commit.com) to run checks before every commit: formatting, linting, secret detection, and blocking of large or personal data files.

Prerequisites: Git and [uv](https://docs.astral.sh/uv/).

1. Install pre-commit:

   ```
   uv tool install pre-commit
   ```

2. Activate the hooks in your clone of the repository:

   ```
   pre-commit install
   ```

3. Check that every file passes:

   ```
   pre-commit run --all-files
   ```

From then on, a commit that fails a check is blocked. Fix the reported issue, run `git add` again, then commit.

## Running the tests

1. Install the project and its development dependencies:

   ```
   uv sync
   ```

2. Run the tests:

   ```
   uv run pytest
   ```

The CV template is `src/job_application_agent/templates/cv_template.docx`. It can be edited in Word: type each `{{ ... }}` or `{% ... %}` tag in one go, without changing its formatting in the middle, then run the tests to check that every tag still works.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request, and [SECURITY.md](SECURITY.md) to report a vulnerability.
