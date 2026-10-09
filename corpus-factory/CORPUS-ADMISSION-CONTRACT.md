# Corpus Fleet Admission Contract

A repository is not an admitted corpus project until all gates below pass.

## Gate 1 — component-specific licensing

Required root files:

- `LICENSE`
- `LICENSE-CODE`
- `LICENSE-CONTENT.md`
- `LICENSING.md`
- `NOTICE`

The default project-owned architecture is PolyForm Noncommercial 1.0.0 for project-original software and CC BY-NC 4.0 for project-original copyrightable corpus content, metadata, annotations, documentation, and research outputs, to the extent the project owns those rights.

This default never relicenses third-party or public-domain material. Upstream CC, public-domain/CC0, museum, publisher, database, software, image, transcription, edition, and other source-specific rights remain controlling for those components. Source-specific rights must be represented in NOTICE, provenance/rights metadata, or both.

## Gate 2 — individual corpus AI skill

Required paths declared by the master registry:

- individual skill instructions
- generated research-bundle index
- authority profile
- member validation entry point

The skill must preserve corpus-native evidence authority, uncertainty, exclusions, source dependence, and rights constraints.

## Gate 3 — master AI membership

The repository must appear exactly once in `combined-ai-skill/registry/corpus-projects.json` with the required skill paths, contract/version information, and admission metadata.

Membership means interoperability only. It never implies linguistic, chronological, genetic, graphical, or decipherment relationships.

## Gate 4 — validation

The master structural validator and fleet-admission validator must pass. Fleet admission checks the current main branch of every registered repository for the required licensing and AI-skill paths.

A new repository may exist as a staging project before these gates pass, but it must not be described as fleet-integrated, master-AI-ready, or a completed corpus release.

## Release rule

No new corpus may be promoted to 1.0.0 until all four gates pass. A failure reopens the admission gate; it must not be waived merely to advance a version number.


## Enforcement

The master `Sync AI skill` workflow runs both the local orchestration validator and `combined-ai-skill/scripts/validate_fleet_admission.py`. The fleet validator inspects each registered repository's current `main` tree and fails closed when required licensing or AI-skill paths are absent.
