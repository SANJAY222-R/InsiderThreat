"""
Project Structure Validator
===========================

Validates that the project directory structure is complete
and all required files exist.

Usage:
    python scripts/validate_structure.py
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

REQUIRED_PATHS = [
    # Root
    ".gitignore",
    "README.md",
    "LICENSE",
    "pyproject.toml",
    "Makefile",
    ".editorconfig",
    ".env.example",
    "CONTRIBUTING.md",
    "CHANGELOG.md",

    # Backend
    "backend/__init__.py",
    "backend/app/__init__.py",
    "backend/app/main.py",
    "backend/app/core/config.py",
    "backend/app/core/security.py",
    "backend/app/core/logging.py",
    "backend/app/core/exceptions.py",
    "backend/app/core/dependencies.py",
    "backend/app/models/base.py",
    "backend/app/schemas/common.py",
    "backend/app/api/v1/router.py",
    "backend/app/services/auth_service.py",
    "backend/app/repositories/base.py",
    "backend/app/middleware/cors.py",

    # AI
    "ai/__init__.py",
    "ai/models/base_model.py",
    "ai/models/thgnn.py",
    "ai/models/node_encoder.py",
    "ai/models/edge_encoder.py",
    "ai/models/temporal_encoder.py",
    "ai/training/trainer.py",
    "ai/inference/predictor.py",
    "ai/explainability/explainer.py",
    "ai/data/dataset_loader.py",

    # Graph
    "graph/__init__.py",
    "graph/builders/base_builder.py",
    "graph/builders/node_builder.py",
    "graph/builders/edge_builder.py",
    "graph/builders/temporal_builder.py",
    "graph/analytics/centrality.py",
    "graph/exporters/neo4j_exporter.py",
    "graph/schemas/node_types.py",
    "graph/schemas/edge_types.py",

    # Configs
    "configs/config.yaml",
    "configs/development.yaml",
    "configs/production.yaml",
    "configs/model.yaml",
    "configs/graph.yaml",
    "configs/logging.yaml",
    "configs/security.yaml",
    "configs/dataset.yaml",

    # Dataset metadata
    "dataset/metadata/schema.yaml",
    "dataset/metadata/dataset_info.yaml",

    # Tests
    "tests/conftest.py",
    "tests/unit/backend/test_exceptions.py",

    # Deployment
    "deployment/docker/Dockerfile.backend",
    "deployment/docker/Dockerfile.frontend",
    "deployment/docker/nginx/nginx.conf",
    "deployment/docker-compose.yml",

    # CI/CD
    ".github/workflows/ci.yml",
    ".github/workflows/cd.yml",

    # Docs
    "docs/architecture/system_overview.md",
    "docs/developer/setup_guide.md",
    "docs/developer/coding_standards.md",

    # Frontend
    "frontend/package.json",
]


def validate() -> None:
    """Validate project structure completeness."""
    print("🔍 Validating project structure...\n")

    missing = []
    found = 0

    for rel_path in REQUIRED_PATHS:
        full_path = PROJECT_ROOT / rel_path
        if full_path.exists():
            found += 1
        else:
            missing.append(rel_path)
            print(f"  ❌ Missing: {rel_path}")

    total = len(REQUIRED_PATHS)
    print(f"\n📊 Results: {found}/{total} files found")

    if missing:
        print(f"\n⚠️  {len(missing)} files missing!")
        return

    print("\n✅ All required files present!")


if __name__ == "__main__":
    validate()
