# Naming Conventions

## Files & Directories

| Category | Convention | Example |
|----------|-----------|---------|
| Python modules | snake_case | `user_service.py` |
| Python packages | snake_case | `graph/builders/` |
| Python classes | PascalCase | `class UserService` |
| Python functions | snake_case | `def get_user()` |
| Python constants | UPPER_SNAKE | `MAX_RETRIES = 3` |
| React components | PascalCase | `GraphViewer.tsx` |
| React hooks | camelCase with `use` | `useAuth.ts` |
| CSS classes | kebab-case | `.risk-score-badge` |
| YAML configs | snake_case | `model.yaml` |
| Database tables | snake_case | `predictions` |
| API endpoints | kebab-case | `/api/v1/graph-query` |
| Docker services | kebab-case | `itd-backend` |
| Git branches | type/description | `feature/graph-builder` |

## Prefixes & Suffixes

| Pattern | Usage | Example |
|---------|-------|---------|
| `Base*` | Abstract base class | `BaseModel`, `BaseRepository` |
| `*Service` | Business logic layer | `PredictionService` |
| `*Repository` | Data access layer | `UserRepository` |
| `*Error` | Custom exception | `GraphBuildError` |
| `*Schema` | Pydantic model | `UserCreate` (implicit) |
| `test_*` | Test function | `test_user_creation` |
| `Test*` | Test class | `TestUserService` |
| `I*` | Interface (rare) | `IGraphBuilder` |
