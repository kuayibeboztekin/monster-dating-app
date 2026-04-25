# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monster Dating App — a dating platform for supernatural beings. The project is in early development (V1.0 planning/scaffolding phase). All source code and documentation are written in German.

## Running Code

The project uses a local virtual environment at `.venv/` with Python 3.14.

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run a module from src/
python src/vampir.py

# Run tests (currently empty, tests/ dir exists but has no test files yet)
python -m pytest tests/
```

Since `vampir.py` imports from `monster` (not `src.monster`), run files from the `src/` directory or set `PYTHONPATH=src` when executing from the project root:

```bash
PYTHONPATH=src python src/vampir.py
```

## Architecture

The domain model follows a class hierarchy defined in `docs/klassendiagramm.md`:

- **`Monster` (abstract base)** — `src/monster.py` — common attributes: `id`, `name`, `monsterTyp`, `alter`, `region`, `aktiv`; core methods: `registrieren`, `anmelden`, `sucheMatches`, `swipeRechts/Links`, `blockieren`, `melden`
- **Concrete subclasses** — `Vampir`, `Werwolf`, `Zombie`, `Geist` (currently only `Vampir` exists in `src/vampir.py`)
- **Supporting classes** (not yet implemented): `Profil`, `Match`, `Nachricht`, `Suchfilter`, `Meldung`, `Administrator`

Key design rules from the class diagram:
- `Monster` owns exactly one `Profil` (composition — a profile cannot exist without its monster)
- `Match` owns its `Nachricht` objects (composition)
- Private chat (`Nachricht`) is only unlocked after a successful mutual match
- Natural-enemy pairs must be excluded from match suggestions and search results

Enumerations to implement: `MonsterTyp`, `MatchStatus`, `Aktivitaetsrhythmus`, `StandortSichtbarkeit`, `Verifizierungsstatus`, `Meldungsstatus`, `Meldungsgrund` — values are documented in `docs/klassendiagramm.md`.

## Branch Strategy

Feature branches are named `feature/<monster-type>` (e.g. `feature/vampir`, `feature/werwolf`). Each branch is expected to implement one concrete monster subclass.
