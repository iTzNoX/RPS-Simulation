class Creature:
    """
    Represents a single creature in the simulation.
    Handles everything regarding the Creatures
    """
    id_counter = 0

    def __init__(self, strategy: str, generation: int = 1):
        """
        Initializes a Creature instance.

        Attributes:
            id (int): 6-digit long unique identifier of the creature
            strategy (str): Has to be R, P or S, representing Rock, Paper or Scissors.
            food_amount (int): the current amount of food the creatues owns. Needed for reproduction.
            generation (int): current generation of the creature.
            alive (bool): defines if the Creature is currently alive or not.
        """
        self.id = f"{Creature.id_counter:06d}"
        Creature.id_counter += 1

        self.food_amount = 0
        self.generation = generation
        self.alive = True
        if strategy not in {"R", "P", "S"}:
            raise ValueError("Strategy must be 'R', 'P', or 'S'.")
        self.strategy = strategy

    def kill(self):
        self.alive = False

    def play(self, opponent) -> str:
        """
        Plays one round against another creature.

        Arguments:
            opponent (Creature): The opposing creature.
        Returns:
            str: 'win', 'lose', or 'draw' depending on the result.
        """
        rules = {"S": "P", "P": "R", "R": "S"}
        if self.strategy == opponent.strategy:
            self.food_amount += 1
            return "draw"
        elif rules[self.strategy] == opponent.strategy:
            self.food_amount += 2
            return "win"
        else:
            return "lose"

    def reproduce(self):
        """
        Generates offspring based on current food_amount.
        Each food unit produces one child with the same strategy.
        The parent creature dies after reproduction.

        Returns:
            list[Creature]: List of offspring creatures.
        """
        offspring = []
        for _ in range(self.food_amount):
            child = Creature(strategy = self.strategy,
                             generation=self.generation+1)
            offspring.append(child)
        self.kill()
        return offspring

    def info(self) -> dict:
        """
        Returns a snapshot of the creature's current state.

        Returns:
            dict: Contains id, strategy and generation.
        """
        return {
            "id": self.id,
            "strategy": self.strategy,
            "generation": self.generation,
        }
