# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bankroll Simulator — a Python application that simulates betting games and tracks bankroll changes through configurable gaming sessions and strategies. Pure Python (standard library only, no external dependencies). Python 3.10+.

## Running

```bash
python3 generate_simulation.py
```

There is no build step, no test framework, and no linter configured.

## Architecture

**Entry point:** `generate_simulation.py` — creates a `Bank` instance and will eventually run a simulation.

**Core modules (`src/`):**

- `Bank.py` — Central `Bank` class managing bankroll state (deposit, withdraw, play). The `play()` method is currently a stub.
- `finder.py` — Loads JSON config files from disk, searches by `name` field, caches loaded data in a module-level dict. `find_game_by_name()` wraps `find_item_by_name()` with schema validation.
- `schema_validator.py` — Validates game JSON configs. Enforces two game schemas: multi-bet-type and single-bet-type. Probabilities must sum to ~1.0 (multi-bet) or not exceed 1.0 (single-bet, where losing is implicit).

**Config-driven design (`config/`):**

All game definitions, session strategies, and simulation plans are JSON files loaded at runtime via `finder.py`.

- `config/games/` — Game definitions. Two types distinguished by the `multi-bet-type` boolean:
  - **Multi-bet** (e.g., Baccarat): has `bet-types` dict where each bet has `multiplier` and `chance`, all chances must sum to ~1.0.
  - **Single-bet** (e.g., Slots, MTT): has `possible-results` list where each result has `name`, `multiplier`, and `chance`, total chance can be ≤1.0.
- `config/sessions/` — Session configs defining a betting strategy: which game/bet-type to play, bet size, min/max quantity of bets, stop-loss and stop-win percentages.
- `config/simulations/` — Simulation configs defining a sequence of actions (`session` or `aport`) with a starting bankroll.

**Data flow:** Simulation config → references session configs by name → sessions reference game configs by name → game configs validated against schema on load.
