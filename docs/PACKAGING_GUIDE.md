# Deterministic Packaging & CSC Interop

Phase 10 introduces reproducible export bundles for CrapsSim-Evo.

## Deterministic Mode
Enable with:
```bash
python -m cli.export_bundle runs/g010 --deterministic
```
- Omits `created_utc` from `bundle_meta.json`.
- Sorts file entries before zipping.
- Uses stable JSON key ordering.

## Interop Manifest
`interop_manifest.json`

```
{
  "schema_version": "0.1",
  "bundle_id": "ab12...def",
  "generation": "g010",
  "compat": "csc>=0.30.0",
  "contents": ["specs", "dna", "metrics", "convergence"],
  "created_by": "crapssim-evo",
  "deterministic": true
}
```

## Determinism Guarantees
- Identical inputs → identical bundle bytes & hash.
- SHA-256 hash stored as `bundle_id`.
- Pure stdlib implementation.
