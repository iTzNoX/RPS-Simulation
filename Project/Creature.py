
# Handles the creation and actions of the Creatures
class Creature:
    id_counter = 0

    def __init__(self, strategy: str):
        Creature.increase_id_counter()
        self.id = f"{Creature.id_counter:06d}"
        self.strategy = strategy
        self.food_amount = 0
        self.generation = 1
        self.alive = True

    @staticmethod
    def increase_id_counter():
        if Creature.id_counter > 999999:
            raise ValueError("Creature limit reached")
        Creature.id_counter += 1

    def play(self, opponent) -> str:
        rules = {"S": "P", "P": "R", "R": "S"}
        #draw
        if self.strategy == opponent.strategy:
            self.food_amount += 1
            return "draw"
        #win
        elif rules[self.strategy] == opponent.strategy:
            self.food_amount += 2
            return "win"
        #lose
        else:
            return "lose"
