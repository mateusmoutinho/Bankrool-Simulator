from .finder import find_game_by_name


def _compute_ev(possible_results: list) -> float:
    ev = sum(r['chance'] * r['multiplier'] for r in possible_results) - 1
    return round(ev, 6)


def get_game_ev(games_dir: str, game_name: str) -> dict:
    game = find_game_by_name(games_dir, game_name)

    if game.get('multi-bet-type'):
        bet_types = {}
        for bet_type, config in game['bet-types'].items():
            bet_types[bet_type] = _compute_ev(config['possible-results'])
        return {"name": game['name'], "bet-types": bet_types}

    return {"name": game['name'], "ev": _compute_ev(game['possible-results'])}

def get_all_games_ev(games_dir: str) -> dict:
    games = os.listdir(games_dir)
    games_ev = {}
    for game in games:
        games_ev[game] = get_game_ev(games_dir, game)
    return games_ev