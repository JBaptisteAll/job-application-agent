# Contributing

Thanks for your interest in improving job-application-agent. This guide explains how to propose a change.

## Before you start

- Every change starts with an issue. Check the [existing issues](https://github.com/JBaptisteAll/job-application-agent/issues) first, then open a new one with the **Task** or **Bug report** form if needed.
- Set up your environment by following the [development setup](README.md#development-setup) section of the README. The pre-commit hooks must be installed before your first commit.
- Never commit personal data: CVs, LinkedIn archives, or generated profiles. The hooks block the most common cases, but you remain responsible for what you push.

## Branch naming

Create your branch from an up-to-date `main`, using the format `type/issue-number-short-summary`:

```
feat/14-parse-linkedin-archive
fix/27-encoding-error-in-profile
docs/9-community-files
```

## Commit messages

Commits follow the [Conventional Commits](https://www.conventionalcommits.org) format: `type: short description in the imperative mood`.

| Type | Use it for |
|---|---|
| `feat` | A new feature |
| `fix` | A bug fix |
| `docs` | Documentation only |
| `ci` | GitHub Actions workflows |
| `chore` | Maintenance that does not change behavior |
| `refactor` | Code changes that neither fix a bug nor add a feature |
| `test` | Adding or updating tests |

Example: `feat: add LinkedIn archive parser`

## Pull request process

1. Push your branch and open a pull request against `main`.
2. Fill in the pull request template, including `Closes #<issue-number>` so the issue closes automatically.
3. Make sure the CI checks pass.
4. The maintainer reviews the change and may ask for updates.
5. Once approved, the maintainer merges it with a merge commit.

## Reporting a security issue

Do not open a public issue for security vulnerabilities. Follow the process described in [SECURITY.md](SECURITY.md).
