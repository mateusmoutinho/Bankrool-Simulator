class Bank:
    def __init__(self, amount,config='config'):
        self.amount = amount
        self.config = config

    def deposit(self,amount):
        self.amount += amount

    def withdraw(self,amount):
        self.amount -= amount
    
    def play(game:str,bet_type:str,amount:float)->float:
        found_game = find_game_by_name(self.config,game)

        if bet_type:
            possible_results = found_game['bet-types'][bet_type]['possible-results']
        else:
            possible_results = found_game['possible-results']
        
        
        