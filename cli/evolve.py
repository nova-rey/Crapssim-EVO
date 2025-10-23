from __future__ import annotations

import argparse

from evo.config import load_config
from evo.logging import setup_logging


def main() -> None:
    parser = argparse.ArgumentParser(description="CrapsSim-Evo CLI (pre-spec scaffolding)")
    parser.add_argument("--config", type=str, help="Path to YAML config", default=None)
    parser.add_argument("--bundle-in", type=str, help="Path to input bundle (.zip)", default=None)
    parser.add_argument("--bundle-out", type=str, help="Path to output bundle (.zip)", default=None)
    parser.add_argument("--run-id", type=str, help="Run identifier", default=None)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    args = parser.parse_args()

    level = "DEBUG" if args.verbose else "INFO"
    setup_logging(level)

    cfg = load_config(args.config)
    if args.run_id:
        cfg["run_id"] = args.run_id

    # Placeholder behavior only
    print("CrapsSim-Evo scaffolding is installed.")
    print(f"run_id={cfg.get('run_id')}, bundle_in={args.bundle_in}, bundle_out={args.bundle_out}")


if __name__ == "__main__":
    main()
