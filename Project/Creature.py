from typing import List, Dict

class Creature:
    """
    Represents a single creature in the simulation.
    Handles everything regarding the Creatures
    """
    id_counter: int = 0

    def __init__(self, strategy: str, generation: int = 1) -> None:
        """
        Initializes a Creature instance.

        Attributes:
            id (int): 6-digit long unique identifier of the creature
            strategy (str): Has to be R, P or S, representing Rock, Paper or Scissors.
            food_amount (int): the current amount of food the creatues owns. Needed for reproduction.
            generation (int): current generation of the creature.
        """
        self.id: str = f"{Creature.id_counter:06d}"
        Creature.id_counter += 1

        self.food_amount: int = 0
        self.generation: int = generation
        if strategy not in {"R", "P", "S"}:
            raise ValueError("Strategy must be 'R', 'P', or 'S'.")
        self.strategy: str = strategy

    def play(self, opponent: "Creature") -> str:
        """
        Plays one round against another creature.

        Arguments:
            opponent (Creature): The opposing creature.
        Returns:
            str: 'win', 'lose', or 'draw' depending on the result.
        """
        if self.strategy == opponent.strategy:
            self.food_amount += 1
            opponent.food_amount += 1
            return "draw"
        elif (self.strategy == "R" and opponent.strategy == "S") or \
             (self.strategy == "S" and opponent.strategy == "P") or \
             (self.strategy == "P" and opponent.strategy == "R"):
            self.food_amount += 2
            opponent.food_amount += 0
            return "win"
        else:
            self.food_amount += 0
            opponent.food_amount += 2
            return "lose"

    def reproduce(self) -> list["Creature"]:
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
        self.food_amount = 0
        return offspring

    def info(self) -> dict[str, str | int]:
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
