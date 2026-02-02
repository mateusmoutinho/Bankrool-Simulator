#!/usr/bin/env python3
"""Example usage and edge case tests for schema validation."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from schema_validator import validate_game_schema


def test_valid_cases():
    """Test valid game configurations."""
    print("\n" + "="*60)
    print("TESTING VALID CASES")
    print("="*60)
    
    # Valid multi-bet game
    valid_multi_bet = {
        "name": "Roulette",
        "multi-bet-type": True,
        "bet-types": {
            "red": {"multiplier": 2.0, "chance": 0.47},
            "black": {"multiplier": 2.0, "chance": 0.47},
            "green": {"multiplier": 35.0, "chance": 0.06}
        }
    }
    
    try:
        validate_game_schema(valid_multi_bet)
        print("✅ Valid multi-bet game passed")
    except ValueError as e:
        print(f"❌ Valid multi-bet game failed: {e}")
    
    # Valid single-bet game
    valid_single_bet = {
        "name": "Coin Flip",
        "multi-bet-type": False,
        "possible-results": [
            {"name": "win", "chance": 0.5, "multiplier": 2.0}
        ]
    }
    
    try:
        validate_game_schema(valid_single_bet)
        print("✅ Valid single-bet game passed")
    except ValueError as e:
        print(f"❌ Valid single-bet game failed: {e}")


def test_invalid_cases():
    """Test invalid game configurations."""
    print("\n" + "="*60)
    print("TESTING INVALID CASES (should fail)")
    print("="*60)
    
    test_cases = [
        # Missing name
        {
            "test_name": "Missing name field",
            "data": {
                "multi-bet-type": True,
                "bet-types": {}
            }
        },
        # Invalid multi-bet-type
        {
            "test_name": "Invalid multi-bet-type (string instead of bool)",
            "data": {
                "name": "Test",
                "multi-bet-type": "yes",
                "bet-types": {}
            }
        },
        # Multi-bet with probabilities > 1
        {
            "test_name": "Multi-bet probabilities sum > 1",
            "data": {
                "name": "Invalid Game",
                "multi-bet-type": True,
                "bet-types": {
                    "option1": {"multiplier": 2.0, "chance": 0.6},
                    "option2": {"multiplier": 2.0, "chance": 0.6}
                }
            }
        },
        # Single-bet with probabilities > 1
        {
            "test_name": "Single-bet probabilities sum > 1",
            "data": {
                "name": "Invalid Slots",
                "multi-bet-type": False,
                "possible-results": [
                    {"name": "win1", "chance": 0.7, "multiplier": 2.0},
                    {"name": "win2", "chance": 0.5, "multiplier": 3.0}
                ]
            }
        },
        # Negative multiplier
        {
            "test_name": "Negative multiplier",
            "data": {
                "name": "Bad Game",
                "multi-bet-type": False,
                "possible-results": [
                    {"name": "loss", "chance": 0.5, "multiplier": -1.0}
                ]
            }
        },
        # Duplicate result names
        {
            "test_name": "Duplicate result names",
            "data": {
                "name": "Duplicate Game",
                "multi-bet-type": False,
                "possible-results": [
                    {"name": "win", "chance": 0.3, "multiplier": 2.0},
                    {"name": "win", "chance": 0.2, "multiplier": 3.0}
                ]
            }
        },
        # Missing required field
        {
            "test_name": "Missing multiplier field",
            "data": {
                "name": "Incomplete Game",
                "multi-bet-type": False,
                "possible-results": [
                    {"name": "win", "chance": 0.5}
                ]
            }
        },
        # Chance out of range
        {
            "test_name": "Chance > 1",
            "data": {
                "name": "Invalid Chance",
                "multi-bet-type": False,
                "possible-results": [
                    {"name": "win", "chance": 1.5, "multiplier": 2.0}
                ]
            }
        }
    ]
    
    for test_case in test_cases:
        try:
            validate_game_schema(test_case["data"])
            print(f"❌ {test_case['test_name']}: Should have failed but passed!")
        except ValueError as e:
            print(f"✅ {test_case['test_name']}: Correctly rejected")
            print(f"   Error: {e}")


def main():
    """Run all example tests."""
    print("="*60)
    print("SCHEMA VALIDATOR EXAMPLES AND EDGE CASES")
    print("="*60)
    
    test_valid_cases()
    test_invalid_cases()
    
    print("\n" + "="*60)
    print("ALL EXAMPLE TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()
