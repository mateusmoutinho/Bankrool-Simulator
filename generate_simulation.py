from src.Bank import Bank
from src.finder import find_game_by_name

bank = Bank(1000)

print(find_game_by_name("config/games", "Baccarat"))
