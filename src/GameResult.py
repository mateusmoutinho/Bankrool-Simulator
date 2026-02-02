
class GameResult:
    def __init__(self,game:str,bet_type:str,bet:float,win:float):
        self.game = game
        self.bet_type = bet_type
        self.bet = bet
        self.win = win
    
    def __str__(self):
        return f"Game: {self.game}, Bet Type: {self.bet_type}, Bet: {self.bet}, Win: {self.win}"