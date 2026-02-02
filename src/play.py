from .finder import find_game_by_name, find_simulation_by_name
import secrets
    
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
    sorteio = secrets.SystemRandom().random()
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

def play_session(sessions_dir:str,games_dir:str,session:str,bankroll:float)->dict:
    """
    Plays a complete session with stop-loss and stop-gain checks.
    
    Args:
        sessions_dir: Directory containing session configurations
        games_dir: Directory containing game configurations
        session: Name of the session to play
        bankroll: Initial bankroll amount
        
    Returns:
        List of bet results with game, bet-type, bet-size, result, payment, and bankroll
        
    The session terminates when:
    - Stop-loss is hit (bankroll <= initial_bankroll - stop-loss-size or bankroll <= initial_bankroll * (1 - stop-loss-percent))
    - Stop-gain is hit (bankroll >= initial_bankroll + stop-win-size or bankroll >= initial_bankroll * (1 + stop-gain-percent))
    - All bets are completed
    - Bankroll is insufficient for a bet (bet is skipped)
    """
    from .finder import find_session_by_name
    
    # Load session configuration
    session_config = find_session_by_name(sessions_dir, session)
    
    # Store initial bankroll for stop-loss/stop-gain calculations
    initial_bankroll = bankroll
    
    # Extract stop conditions
    stop_loss_size = session_config.get('stop-loss-size')
    stop_win_size = session_config.get('stop-win-size')
    stop_loss_percent = session_config.get('stop-loss-percent')
    stop_gain_percent = session_config.get('stop-gain-percent')
    
    # Results list
    results = []
    
    # Process each bet configuration
    for bet_config in session_config['bets']:
        game_name = bet_config['game']
        bet_type = bet_config.get('bet-type')
        
        # Determine bet size
        if 'bet-size' in bet_config:
            bet_size = bet_config['bet-size']
        else:
            # Calculate bet size from percentage
            bet_percent = bet_config['bet-percent']
            bet_size = bankroll * bet_percent
        
        # Determine how many times to place this bet
        min_quantity = bet_config.get('min-quantity', 1)
        max_quantity = bet_config.get('max-quantity', min_quantity)
        
        # Random quantity between min and max
        quantity = secrets.SystemRandom().randint(min_quantity, max_quantity)
        
        # Place bets
        for _ in range(quantity):
            # Check stop-loss conditions
            if stop_loss_size is not None:
                if bankroll <= initial_bankroll - stop_loss_size:
                    return results
            
            if stop_loss_percent is not None:
                if bankroll <= initial_bankroll * (1 - stop_loss_percent):
                    return results
            
            # Check stop-gain conditions
            if stop_win_size is not None:
                if bankroll >= initial_bankroll + stop_win_size:
                    return results
            
            if stop_gain_percent is not None:
                if bankroll >= initial_bankroll * (1 + stop_gain_percent):
                    return results
            
            # Skip bet if bankroll is insufficient
            if bet_size > bankroll:
                continue
            
            # Deduct bet from bankroll
            bankroll -= bet_size
            
            # Play the game
            game_result = play_game(games_dir, game_name, bet_type, bet_size)
            
            # Add payment to bankroll
            bankroll += game_result['payment']
            
            # Record the result
            results.append({
                'game': game_name,
                'bet-type': bet_type,
                'bet-size': bet_size,
                'result': game_result['result'],
                'payment': game_result['payment'],
                'bankroll': bankroll
            })

    return results

def play_simulation(simulations_dir:str,sessions_dir:str,games_dir:str,simulation:str)->list:
    sim_config = find_simulation_by_name(simulations_dir, simulation)
    bankroll = sim_config['start-bankroll']

    results = []

    for action in sim_config['actions']:
        action_type = action['type']

        if action_type == 'play':
            session_name = action['name']
            session_result = play_session(sessions_dir, games_dir, session_name, bankroll)

            if session_result:
                bankroll = session_result[-1]['bankroll']

            results.append({
                'type': 'play',
                'name': session_name,
                'bets': session_result,
                'bankroll': bankroll
            })

        elif action_type == 'withdraw':
            size = action['size']
            bankroll -= size
            results.append({
                'type': 'withdraw',
                'size': size,
                'bankroll': bankroll
            })

        elif action_type == 'aport':
            size = action['size']
            bankroll += size
            results.append({
                'type': 'aport',
                'size': size,
                'bankroll': bankroll
            })

    return results