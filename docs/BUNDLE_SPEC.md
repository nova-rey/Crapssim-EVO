# Bundle Specification (.zip)

## Format
`.zip` chosen for simplicity; files are small.

## Required Layout

run/
journal.csv
report.json
manifest.json
spec.json
checksums.txt
CONTENTS.json
meta/
bundle.json
README.txt

## meta/bundle.json
```json
{
  "bundle_schema_version": "1.0",
  "producer": "CSC",
  "run_id": "2025-10-23-g001",
  "created_utc": "2025-10-23T15:12:03Z",
  "format": "zip",
  "contents": {
    "journal": "run/journal.csv",
    "report": "run/report.json",
    "manifest": "run/manifest.json"
  },
  "schemas": {"journal":"1.1","report":"1.1","spec":"1.0"}
}

Safety
• Verify extraction paths stay inside staging dir.
• Reject missing required files.
• Preserve any unknown files verbatim.
• Include SHA256 checksums for integrity.

CLI Example

csc run --from-bundle g001_input.zip --bundle-out g001_results.zip
