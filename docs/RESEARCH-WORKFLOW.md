# Researcher workflow

1. Read `docs/COVERAGE.md` and `ai-skill/references/authority-profile.json` to establish what is verified.
2. Select a record in `data/inscriptions.json`, and follow its bibliographic locators.
3. Inspect primary publication, photograph or critical edition independently; note rights before copying.
4. Capture diplomatic signs and line boundaries separately from editorial normalization, with per-reading uncertainty and source locator.
5. Preserve alternative editions and restoration proposals as separate attributed claims.
6. Run `python ai-skill/scripts/validate_bundle.py` and `python scripts/validate_corpus.py`.
7. For AI questions, provide `ai-skill/SKILL.md`, the bundle index, and cited record evidence; reject unsupported translations.
8. For cross-corpus comparisons, load the master combined AI skill, check native units and source independence, and report blocked inference explicitly.

A bibliographic target is not an authenticated inscription reading. All three records remain provisional.
