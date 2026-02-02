# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Project

```bash
python3 generate_simulation.py
```

No external dependencies — uses only Python 3.10+ standard library (`random`, `json`, `os`). No build step, package manager, or test framework is configured.

## Architecture

Bankrool-Simulator is a gambling/betting session simulator that models casino games (Baccarat, Slots, MTT, Sit & Go) with probability-based outcomes and bankroll management.

### Core Flow

`generate_simulation.py` → `play_session()` → iterates session bets → `play_game()` per bet → returns bet history with bankroll tracking.

### Source Modules (`src/`)

- **play.py** — Two main functions: `play_game()` executes a single game by generating a random outcome weighted by configured probabilities; `play_session()` runs a full betting session with stop-loss/stop-gain conditions, bankroll tracking, and bet skipping when funds are insufficient.
- **schema_validator.py** — Validates game and session JSON configs with type checking, required field enforcement, and probability constraints (accumulated chance ≤ 1.01 for float tolerance).
- **finder.py** — Loads JSON configs from `config/` directories with in-memory caching (`loaded_data` dict) to avoid redundant file I/O.

### Configuration (`config/`)

- **`config/games/`** — Game definitions in JSON. Two formats: single-bet (e.g., slots with one `possible-results` array) and multi-bet (`"multi-bet-type": true` with `bet-types` map, e.g., baccarat with player/banker/tie).
- **`config/sessions/`** — Session strategies defining ordered bets with stop conditions. Each bet references a game name, bet type, sizing (fixed `bet-size` or percentage `bet-percent`), and repetition range (`min-quantity`/`max-quantity`).
- **`config/simulations/`** — Tracks simulation state.

### Key Design Details

- Probability engine: `random.random()` generates uniform [0,1), accumulated against result chances to pick an outcome. Remaining probability space is an implicit loss (pays 0).
- Stop conditions: sessions require at least one of `stop-loss-size`, `stop-loss-percent`, `stop-win-size`, `stop-gain-percent`. Both fixed-amount and percentage-of-bankroll thresholds are supported.
- Bet sizing: either fixed (`bet-size`) or proportional to current bankroll (`bet-percent`).
