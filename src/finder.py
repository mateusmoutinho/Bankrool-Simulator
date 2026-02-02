import os
import json
from src.schema_validator import validate_game_schema,validate_session_schema

loaded_data = {}

def find_item_by_name(dir:str,name:str)->dict:

    for filename in os.listdir(dir):

        if not filename.endswith('.json'):
            continue
        
        filepath = os.path.join(dir, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        try:
            item_name = json_data.get('name')
        except:
            raise ValueError(f"Item '{name}' not found in directory '{dir}'")
        

        if item_name == name:
            if filepath not in loaded_data:
                loaded_data[filepath] = {}
            
            loaded_data[filepath][item_name] = json_data
            return json_data
    
    raise ValueError(f"Item '{name}' not found in directory '{dir}'")   


def find_game_by_name(dir:str,name:str)->dict:
    game = find_item_by_name(dir,name)
    validate_game_schema(game)
    return game

def find_session_by_name(dir:str,name:str)->dict:
    session = find_item_by_name(dir,name)
    validate_session_schema(session)
    return session

def find_simulation_by_name(dir:str,name:str)->dict:
    return find_item_by_name(dir,name)