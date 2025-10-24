# Bundle Specification (v1.0)

This document defines the structure and safety rules for `.zip` bundles exchanged between CrapsSim-Control (CSC) and CrapsSim-Evo (EVO).

## Structure
| Directory | Purpose |
|:--|:--|
| `seed_*/` | Contains `spec.json`, `dna.json`, and related seed data. |
| `run/` | Holds simulator outputs and generated indices. |
| `meta/` | Contains metadata such as `bundle.json`. |

## Safety
- Zip-slip guarded during extraction.
- Unknown files preserved.
- Deterministic path separators (`/`).
- SHA256 checksums for auditability.

## Manifest Example
```json
{
  "bundle_schema_version": "1.0",
  "producer": "EVO",
  "created_utc": "2025-10-24T00:00:00Z",
  "format": "zip"
}
```
