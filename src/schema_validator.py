def validate_game_schema(game: dict) -> bool:
    """
    Validates game schema for both single-bet and multi-bet-type games.
    
    Args:
        game: Dictionary containing game configuration
        
    Returns:
        bool: True if schema is valid
        
    Raises:
        ValueError: If schema validation fails with detailed error message
    """
    # Check required base fields
    if not isinstance(game, dict):
        raise ValueError("Game must be a dictionary")
    
    if "name" not in game:
        raise ValueError("Game must have a 'name' field")
    
    if not isinstance(game["name"], str) or not game["name"].strip():
        raise ValueError("Game 'name' must be a non-empty string")
    
    if "multi-bet-type" not in game:
        raise ValueError(f"Game '{game['name']}' must have a 'multi-bet-type' field")
    
    if not isinstance(game["multi-bet-type"], bool):
        raise ValueError(f"Game '{game['name']}' 'multi-bet-type' must be a boolean")
    
    # Validate based on game type
    if game["multi-bet-type"]:
        _validate_multi_bet_game(game)
    else:
        _validate_single_bet_game(game)
    
    return True


def _validate_multi_bet_game(game: dict) -> None:
    """
    Validates multi-bet-type games (e.g., Baccarat).

    Each bet type must contain a 'possible-results' list where each result
    has 'name', 'chance', and 'multiplier'. Total chance per bet type cannot
    exceed 1.0 (losing is implicit from remaining probability).

    Args:
        game: Dictionary containing game configuration

    Raises:
        ValueError: If validation fails
    """
    game_name = game["name"]

    if "bet-types" not in game:
        raise ValueError(f"Multi-bet game '{game_name}' must have 'bet-types' field")

    bet_types = game["bet-types"]

    if not isinstance(bet_types, dict):
        raise ValueError(f"Game '{game_name}' 'bet-types' must be a dictionary")

    if not bet_types:
        raise ValueError(f"Game '{game_name}' must have at least one bet type")

    for bet_name, bet_config in bet_types.items():
        if not isinstance(bet_name, str) or not bet_name.strip():
            raise ValueError(f"Game '{game_name}' bet type names must be non-empty strings")

        if not isinstance(bet_config, dict):
            raise ValueError(f"Game '{game_name}' bet type '{bet_name}' must be a dictionary")

        if "possible-results" not in bet_config:
            raise ValueError(f"Game '{game_name}' bet type '{bet_name}' must have 'possible-results' field")

        possible_results = bet_config["possible-results"]

        if not isinstance(possible_results, list):
            raise ValueError(f"Game '{game_name}' bet type '{bet_name}' 'possible-results' must be a list")

        if not possible_results:
            raise ValueError(f"Game '{game_name}' bet type '{bet_name}' must have at least one possible result")

        total_chance = 0.0
        result_names = set()

        for idx, result in enumerate(possible_results):
            if not isinstance(result, dict):
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result at index {idx} must be a dictionary"
                )

            # Validate name
            if "name" not in result:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result at index {idx} must have 'name' field"
                )

            result_name = result["name"]
            if not isinstance(result_name, str) or not result_name.strip():
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result at index {idx} name must be a non-empty string"
                )

            if result_name in result_names:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' has duplicate result name: '{result_name}'"
                )

            result_names.add(result_name)

            # Validate chance
            if "chance" not in result:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' must have 'chance' field"
                )

            chance = result["chance"]
            if not isinstance(chance, (int, float)):
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' chance must be a number"
                )

            if not 0 <= chance <= 1:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' chance must be between 0 and 1"
                )

            total_chance += chance

            # Validate multiplier
            if "multiplier" not in result:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' must have 'multiplier' field"
                )

            multiplier = result["multiplier"]
            if not isinstance(multiplier, (int, float)):
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' multiplier must be a number"
                )

            if multiplier < 0:
                raise ValueError(
                    f"Game '{game_name}' bet type '{bet_name}' result '{result_name}' multiplier must be non-negative"
                )

        # Validate total probability per bet type (allow small floating point errors)
        # Loss is implicit from remaining probability, so total chance can be less than 1
        if total_chance > 1.01:
            raise ValueError(
                f"Game '{game_name}' bet type '{bet_name}' total chance across all results cannot exceed 1.0 "
                f"(got {total_chance:.4f})"
            )


def _validate_single_bet_game(game: dict) -> None:
    """
    Validates single-bet-type games (e.g., MTT, Slots).
    
    Args:
        game: Dictionary containing game configuration
        
    Raises:
        ValueError: If validation fails
    """
    game_name = game["name"]
    
    if "possible-results" not in game:
        raise ValueError(f"Single-bet game '{game_name}' must have 'possible-results' field")
    
    possible_results = game["possible-results"]
    
    if not isinstance(possible_results, list):
        raise ValueError(f"Game '{game_name}' 'possible-results' must be a list")
    
    if not possible_results:
        raise ValueError(f"Game '{game_name}' must have at least one possible result")
    
    total_chance = 0.0
    result_names = set()
    
    for idx, result in enumerate(possible_results):
        if not isinstance(result, dict):
            raise ValueError(f"Game '{game_name}' result at index {idx} must be a dictionary")
        
        # Validate name
        if "name" not in result:
            raise ValueError(f"Game '{game_name}' result at index {idx} must have 'name' field")
        
        result_name = result["name"]
        if not isinstance(result_name, str) or not result_name.strip():
            raise ValueError(f"Game '{game_name}' result at index {idx} name must be a non-empty string")
        
        if result_name in result_names:
            raise ValueError(f"Game '{game_name}' has duplicate result name: '{result_name}'")
        
        result_names.add(result_name)
        
        # Validate chance
        if "chance" not in result:
            raise ValueError(f"Game '{game_name}' result '{result_name}' must have 'chance' field")
        
        chance = result["chance"]
        if not isinstance(chance, (int, float)):
            raise ValueError(f"Game '{game_name}' result '{result_name}' chance must be a number")
        
        if not 0 <= chance <= 1:
            raise ValueError(f"Game '{game_name}' result '{result_name}' chance must be between 0 and 1")
        
        total_chance += chance
        
        # Validate multiplier
        if "multiplier" not in result:
            raise ValueError(f"Game '{game_name}' result '{result_name}' must have 'multiplier' field")
        
        multiplier = result["multiplier"]
        if not isinstance(multiplier, (int, float)):
            raise ValueError(f"Game '{game_name}' result '{result_name}' multiplier must be a number")
        
        if multiplier < 0:
            raise ValueError(f"Game '{game_name}' result '{result_name}' multiplier must be non-negative")
    
    # Validate total probability (allow small floating point errors)
    # Note: For single-bet games, total chance can be less than 1 (losing is implicit)
    if total_chance > 1.01:
        raise ValueError(
            f"Game '{game_name}' total chance across all results cannot exceed 1.0 "
            f"(got {total_chance:.4f})"
        )


def validate_session_schema(session: dict) -> bool:
    """
    Validates session schema.
    
    Rules:
    - 'name' is required
    - At least one of: stop-loss-size, stop-loss-percent, stop-gain-percent is required
    - Percent fields (stop-loss-percent, stop-gain-percent) must be >0 and <1
    - 'bets' is required and must be a non-empty list
    - Each bet must have either 'bet-size' or 'bet-percent' (one is required)
    - bet-percent must be >0 and <1
    
    Args:
        session: Dictionary containing session configuration
        
    Returns:
        bool: True if schema is valid
        
    Raises:
        ValueError: If schema validation fails with detailed error message
    """
    # Check that session is a dictionary
    if not isinstance(session, dict):
        raise ValueError("Session must be a dictionary")
    
    # Validate name field
    if "name" not in session:
        raise ValueError("Session must have a 'name' field")
    
    if not isinstance(session["name"], str) or not session["name"].strip():
        raise ValueError("Session 'name' must be a non-empty string")
    
    session_name = session["name"]
    
    # Validate stop-loss-size if present (optional)
    if "stop-loss-size" in session:
        stop_loss_size = session["stop-loss-size"]
        if not isinstance(stop_loss_size, (int, float)):
            raise ValueError(
                f"Session '{session_name}' 'stop-loss-size' must be a number"
            )
        if stop_loss_size <= 0:
            raise ValueError(
                f"Session '{session_name}' 'stop-loss-size' must be greater than 0"
            )
    
    # Validate stop-loss-percent if present (optional)
    if "stop-loss-percent" in session:
        stop_loss_percent = session["stop-loss-percent"]
        if not isinstance(stop_loss_percent, (int, float)):
            raise ValueError(
                f"Session '{session_name}' 'stop-loss-percent' must be a number"
            )
        if not (0 < stop_loss_percent < 1):
            raise ValueError(
                f"Session '{session_name}' 'stop-loss-percent' must be greater than 0 and less than 1"
            )
    
    # Validate stop-gain-percent if present (optional)
    if "stop-gain-percent" in session:
        stop_gain_percent = session["stop-gain-percent"]
        if not isinstance(stop_gain_percent, (int, float)):
            raise ValueError(
                f"Session '{session_name}' 'stop-gain-percent' must be a number"
            )
        if not (0 < stop_gain_percent < 1):
            raise ValueError(
                f"Session '{session_name}' 'stop-gain-percent' must be greater than 0 and less than 1"
            )
    
    # Validate bets field
    if "bets" not in session:
        raise ValueError(f"Session '{session_name}' must have a 'bets' field")
    
    bets = session["bets"]
    
    if not isinstance(bets, list):
        raise ValueError(f"Session '{session_name}' 'bets' must be a list")
    
    if not bets:
        raise ValueError(f"Session '{session_name}' must have at least one bet")
    
    # Validate each bet
    for idx, bet in enumerate(bets):
        if not isinstance(bet, dict):
            raise ValueError(
                f"Session '{session_name}' bet at index {idx} must be a dictionary"
            )
        
        # Check that bet has either bet-size or bet-percent
        has_bet_size = "bet-size" in bet
        has_bet_percent = "bet-percent" in bet
        
        if not (has_bet_size or has_bet_percent):
            raise ValueError(
                f"Session '{session_name}' bet at index {idx} must have either 'bet-size' or 'bet-percent'"
            )
        
        # Validate bet-size if present
        if has_bet_size:
            bet_size = bet["bet-size"]
            if not isinstance(bet_size, (int, float)):
                raise ValueError(
                    f"Session '{session_name}' bet at index {idx} 'bet-size' must be a number"
                )
            if bet_size <= 0:
                raise ValueError(
                    f"Session '{session_name}' bet at index {idx} 'bet-size' must be greater than 0"
                )
        
        # Validate bet-percent if present
        if has_bet_percent:
            bet_percent = bet["bet-percent"]
            if not isinstance(bet_percent, (int, float)):
                raise ValueError(
                    f"Session '{session_name}' bet at index {idx} 'bet-percent' must be a number"
                )
            if not (0 < bet_percent < 1):
                raise ValueError(
                    f"Session '{session_name}' bet at index {idx} 'bet-percent' must be greater than 0 and less than 1"
                )
    
    return True