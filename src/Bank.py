class Bank:
    def __init__(self, amount,config='config'):
        self.amount = amount
        self.config = config

    def deposit(self,amount):
        self.amount += amount

    def withdraw(self,amount):
        self.amount -= amount
    
    def play(game:str,bet_type:str,amount:float)->float:
        
