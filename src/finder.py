import os
import json

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