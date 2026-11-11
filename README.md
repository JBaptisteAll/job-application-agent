# job-application-agent

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
