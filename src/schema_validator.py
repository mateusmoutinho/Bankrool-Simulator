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