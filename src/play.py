from .finder import find_game_by_name
import random
    
def play_game(games_dir:str,game:str,bet_type:str,amount:float)->dict:
    found_game = find_game_by_name(games_dir,game)
    
    if found_game['multi-bet-type'] and not bet_type:
        raise ValueError("these game requires a bet type")

    if found_game['multi-bet-type']:
        try:
            possible_results = found_game['bet-types'][bet_type]['possible-results']
        except:
            raise ValueError(f"Bet type '{bet_type}' not found in game '{game}'")
    else:
        possible_results = found_game['possible-results']
    
    
    ## make a sorteio from 0 to 1 
    sorteio = random.random()
    acumulated = 0
    for result in possible_results:
        if sorteio <= acumulated + result['chance']:
            return {
                "result":result['name'],    
                "payment":amount*result['multiplier']
                }
        acumulated += result['chance']
    return {
        "result":"loss",
        "payment":0
    }