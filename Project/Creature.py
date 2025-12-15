class Creature:
    id_counter = 0

    def __init__(self, strategy: str, generation: int = 1):
        Creature.increase_id_counter()
        self.id = f"{Creature.id_counter:06d}"
        self.food_amount = 0
        self.generation = generation
        self.alive = True
        if strategy not in {"R", "P", "S"}:
            raise ValueError("Strategy must be 'R', 'P', or 'S'.")
        self.strategy = strategy

    @staticmethod
    def increase_id_counter():
        if Creature.id_counter > 999999:
            raise ValueError("Creature limit reached")
        Creature.id_counter += 1

    def kill(self):
        self.alive = False
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

    def reproduce(self):
        offspring = []
        for _ in range(self.food_amount):
            child = Creature(strategy = self.strategy,
                             generation=self.generation+1)
            offspring.append(child)
        self.kill()
        return offspring
