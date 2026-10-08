# Read-only research tools

Use Python 3 (standard library only):

```bash
python scripts/research_api.py inscriptions
python scripts/research_api.py inscriptions --text Xanthos
python scripts/research_api.py lines
python scripts/research_api.py coverage
python scripts/research_api.py kwic --text example
python scripts/research_api.py export
python scripts/research_api.py inscriptions --format csv
python tests/test_research_api.py
```

KWIC currently returns zero hits because no verified lines have been entered; it does **not** show that a word is absent from Milyan. JSON export preserves status and provenance. Line data remain empty until edition-level transcription rights and source verification are resolved. CSV is a convenience format and serializes nested data as JSON strings.
