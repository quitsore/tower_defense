class Player:
    def __init__(self, gold):
        self.gold = gold

    def receive_gold(self, value=10):
        self.gold += value

    def spend_gold(self, tower_cost):
        self.gold -= tower_cost

    def action(self):
        pass
