# Contributing to Insider Threat Detection System

Thank you for your interest in contributing! This document provides guidelines
and workflows for contributing to this project.

## Development Workflow

### Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch for features |
| `feature/*` | New features |
| `bugfix/*` | Bug fixes |
| `hotfix/*` | Production hotfixes |
| `release/*` | Release preparation |

### Commit Conventions

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:** `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

**Scopes:** `backend`, `frontend`, `ai`, `graph`, `config`, `deploy`, `docs`

### Pull Request Process

1. Create a feature branch from `develop`
2. Write code following our coding standards
3. Add/update tests for your changes
4. Run `make check` to verify lint + tests pass
5. Submit a PR with a clear description
6. Await code review from at least one maintainer

## Coding Standards

### Python
- **Formatter:** Black (line length 100)
- **Import sorting:** isort (profile=black)
- **Linting:** Flake8 + MyPy
- **Type hints:** Required on all public functions
- **Docstrings:** Google style, required on all public classes/functions
- **Architecture:** SOLID principles, Clean Architecture

### TypeScript / React
- **Formatter:** Prettier
- **Linting:** ESLint
- **Components:** Functional components with hooks
- **State:** Redux Toolkit for global state
- **Types:** Strict TypeScript — no `any`

## Code Review Standards

- All PRs require at least 1 approval
- CI must pass before merge
- No force-pushes to `main` or `develop`
- Squash and merge for feature branches
