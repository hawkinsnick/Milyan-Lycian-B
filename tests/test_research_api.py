#!/usr/bin/env python3
"""Smoke tests for the committed read-only API."""
import json,subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def run(*args):
    return subprocess.check_output([sys.executable,str(root/'scripts/research_api.py'),*args],text=True)
coverage=json.loads(run('coverage'))
assert coverage['inscription_segments']==3
assert coverage['verified_segments']==0
assert coverage['verified_lines']==0
assert json.loads(run('kwic','--text','unattested-token'))==[]
assert len(json.loads(run('inscriptions')))==3
assert json.loads(run('lines'))==[]
print('PASS: API coverage, KWIC, inscription listing and empty line-layer semantics')
