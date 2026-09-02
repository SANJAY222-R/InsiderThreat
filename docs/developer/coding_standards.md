# Coding Standards

## Python

### Formatting
- **Black** — Line length 100, target Python 3.12
- **isort** — Import sorting with Black-compatible profile

### Type Hints
- Required on ALL public functions and methods
- Use `from __future__ import annotations` for forward references
- Prefer `X | None` over `Optional[X]` (Python 3.12)
- Prefer `list[T]` over `List[T]`

### Docstrings
- Google style docstrings on all public classes and functions
- Include Args, Returns, Raises sections

### Architecture
- **SOLID** principles throughout
- **Clean Architecture** — dependencies point inward
- **Repository Pattern** — data access abstraction
- **Service Layer** — business logic encapsulation
- **Dependency Injection** — via FastAPI Depends()

### Example

```python
def compute_risk_score(
    user_id: str,
    features: dict[str, float],
    threshold: float = 0.5,
) -> float:
    """
    Compute threat risk score for a user.

    Args:
        user_id: Enterprise user identifier.
        features: Feature vector as name-value pairs.
        threshold: Classification threshold.

    Returns:
        Normalized risk score between 0.0 and 1.0.

    Raises:
        ValidationError: If user_id is empty.
        InferenceError: If model prediction fails.
    """
    ...
```

## TypeScript / React

### General
- Strict TypeScript — no `any` types
- Functional components with hooks
- Named exports (no default exports for components)

### State Management
- Redux Toolkit for global state
- React hooks for local state
- RTK Query for API calls (future)

### Naming
- PascalCase for components: `GraphViewer.tsx`
- camelCase for hooks: `useAuth.ts`
- camelCase for utilities: `formatDate.ts`
- SCREAMING_SNAKE for constants
