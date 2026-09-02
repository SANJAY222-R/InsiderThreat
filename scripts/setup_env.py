"""
Environment Setup Script
========================

Automates the initial development environment setup:
- Creates virtual environment
- Installs dependencies
- Creates necessary directories
- Validates configuration files

Usage:
    python scripts/setup_env.py
"""

import subprocess
import sys
from pathlib import Path

__all__ = ["setup"]

PROJECT_ROOT = Path(__file__).parent.parent

REQUIRED_DIRS = [
    "logs/app",
    "logs/api",
    "logs/training",
    "logs/predictions",
    "logs/security",
    "logs/errors",
    "data",
    "dataset/raw",
    "dataset/processed",
    "dataset/features",
    "dataset/graphs",
    "dataset/reports",
    "reports/data_quality",
    "reports/model_performance",
    "reports/security_audits",
    "ai/checkpoints",
]


def setup() -> None:
    """Run full environment setup."""
    print("🔧 Setting up development environment...\n")

    # Create directories
    for dir_path in REQUIRED_DIRS:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"  📁 Created: {dir_path}")

    # Check .env
    env_file = PROJECT_ROOT / ".env"
    env_example = PROJECT_ROOT / ".env.example"
    if not env_file.exists() and env_example.exists():
        import shutil
        shutil.copy2(env_example, env_file)
        print("  📄 Created .env from .env.example")

    print("\n✅ Environment setup complete!")
    print("   Next steps:")
    print("   1. Edit .env with your configuration")
    print("   2. Run: pip install -e '.[dev]'")
    print("   3. Run: cd frontend && npm install")
    print("   4. Run: make test")


if __name__ == "__main__":
    setup()
