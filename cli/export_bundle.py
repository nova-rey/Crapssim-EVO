import argparse
from pathlib import Path

from evo.io.bundles import write_bundle_zip, write_interop_manifest


def main() -> None:
    p = argparse.ArgumentParser(description="Package generation folder")
    p.add_argument("root", type=Path)
    p.add_argument("--deterministic", action="store_true", help="Stable bundle mode")
    args = p.parse_args()

    out_zip = args.root.with_suffix(".zip")
    write_bundle_zip(args.root, out_zip, deterministic=args.deterministic)
    write_interop_manifest(out_zip, args.root.name, args.deterministic)
    print(f"Wrote {out_zip}")
    print("Interop manifest written alongside bundle.")


if __name__ == "__main__":
    main()
