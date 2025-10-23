from __future__ import annotations

import sys
from pathlib import Path


def test_imports():
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    import cli  # noqa: F401
    import evo  # noqa: F401
