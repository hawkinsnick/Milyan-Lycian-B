---
name: milyan-corpus-research
description: Evidence-first Milyan (Lycian B) inscription research and source criticism.
version: 0.3.1
---
# Milyan corpus skill

Load `ai-skill/references/authority-profile.json` and `ai-skill/generated/research-bundle-index.json` first. Canonical evidence is `data/inscriptions.json`, not this skill. Milyan/Lycian B is distinct from Lycian A. Distinguish monument, inscription, face and line; TL 44c and TL 44d share a physical monument. Treat provisional metadata as leads, never verified epigraphy. No text, reading, translation or morphological analysis is authenticated yet. Every assertion must cite a record ID and an edition locator. Keep competing analyses and uncertainty visible. Never infer language relationships from cross-corpus infrastructure. Enforce source-specific rights. For comparison, follow the master skill's comparability gate. Rebuild the bundle index, review this skill and update the master registry when the dataset changes.

## Evidence querying
Use `python scripts/research_api.py coverage`, `inscriptions`, `lines`, `kwic --text QUERY`, or `export`. Source reconciliation is in `research/source-reconciliation.json`. The line layer currently has zero records: zero search results do **not** establish word absence. Do not infer morphology, phonology or translations from metadata alone. Consult `docs/RESEARCH-API.md`.

## Fleet research contract
Follow `ai-skill/references/corpus-project-contract.md`. Read `ai-skill/generated/fleet-contract-index.json` and replay `python ai-skill/scripts/fleet_contract.py` before claiming synchronized authority. Missing or changed hashes mean stale input, not permission to infer missing evidence. This adapter preserves the native bundle schema. Software admission is separate from expert certification, independent witnesses, and source-specific rights clearance.
