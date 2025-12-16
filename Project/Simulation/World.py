from Project.Simulation.Creature import Creature
from collections import Counter
import random

class World:
    """
    Represents a single World with multiple Cycles. One Cycle can be seen as one day.
    Handles everything regarding the World
    """
    id_counter: int = 0

    def __init__(self, start_participants: int = 9999, max_cycles: int = 10, distribution: list[int] = None) -> None:
        """
        Initializes a World instance.

        Attributes:
            Configuration:
                start_participants (int): Total number of participants at start
                    (rounded downwards to nearest multiple of 3).
                max_cycles (int): Number of max World cycles to run.
                distribution (list[int]): Exact number of participants per strategy [R, P, S].
                strategies (list[str]): Ordered list of available strategies.
            runtime state:
                creatures (list[Creature]): List of all Creature objects participating in the World.
                current_cycle (int): Index of the currently processed World cycle.
                current_participants (int): Current number of living creatures.
        """
        self.id: str = f"{World.id_counter:06d}"
        World.id_counter += 1

        self.max_cycles: int = max_cycles
        self.start_participants: int = start_participants - (start_participants % 3)

        self.current_cycle: int = 0
        self.current_participants: int = self.start_participants

        if distribution is None:
            per_strategy = self.start_participants // 3
            self.distribution: list[int] = [per_strategy] * 3
        else:
            if len(distribution) != 3:
                raise ValueError("Distribution must have exactly 3 int values, representing the amount of (R, P, S).")
            if not all(isinstance(x, int) and x >= 0 for x in distribution):
                raise ValueError("Distribution values must be non-negative integers.")
            if sum(distribution) != self.start_participants:
                raise ValueError(
                    f"Sum of distribution ({sum(distribution)}) must equal total participants "
                    f"({self.start_participants}, rounded down to nearest multiple of 3)."
                )
            self.distribution: list[int] = distribution

        self.creatures: list[Creature] = []
        self.strategies: list[str] = ["R", "P", "S"]
        for strategy, count in zip(self.strategies, self.distribution):
            for _ in range(count):
                self.creatures.append(Creature(strategy=strategy))

    def next_cycle(self) -> None:
        """
        Executes a single World cycle (one day).

        In each cycle, all currently living creatures are randomly paired and play
        exactly one round of Rock-Paper-Scissors. Each creature gains food based on
        the outcome of its match

        After all matches are completed, every creature reproduces. The number of
        offspring produced by a creature equals its accumulated food amount.
        The parent generation is then completely replaced by the offspring
        generation.

        Notes:
        - Each creature participates in at most one match per cycle.
        - No creature survives into the next cycle. Population continuity is
          achieved solely through reproduction.
        - The total population size depends entirely on the food-to-offspring
          conversion rules defined in the Creature class.

        Attributes:
            runtime state:
                creatures (list[Creature]): Current population at the beginning of the cycle.
                current_participants (int): reflects the size of the current population.
                current_cycle (int): reflects the current cycle for later output in info.
            Local variables:
                creature_pool (list[Creature]): Shuffled working copy of the current
                    population used to form random, non-overlapping match pairs.
                already_played (list[Creature]): Collection of all creatures that
                    participated in a match during this cycle and are eligible for reproduction.
                offspring_list (list[Creature]): Accumulates all offspring generated
                    during the reproduction phase and becomes the new population.
        """
        creature_pool: list[Creature] = self.creatures[:]
        already_played: list[Creature] = []
        offspring_list: list[Creature] = []

        random.shuffle(creature_pool)

        while len(creature_pool) > 1:
            c1 = creature_pool.pop()
            c2 = creature_pool.pop()
            c1.play(c2)
            already_played.extend([c1, c2])

        if len(creature_pool) == 1:
            last = creature_pool.pop()
            last.food_amount += 1
            already_played.append(last)

        for creature in already_played:
            offspring = creature.reproduce()
            offspring_list.extend(offspring)

        self.creatures.clear()
        self.creatures.extend(offspring_list)
        self.current_participants = len(self.creatures)
        self.current_cycle += 1

    def info(self) -> dict[str, object]:
        """
        Returns a snapshot of the current World state.

        Returns:
            dict: Contains current cycle, total creatures, strategy counts,
                  and info of 3 random sample creatures.
        """

        total_creatures = self.current_participants
        strategy_counts = Counter(c.strategy for c in self.creatures)

        sample_creatures = random.sample(self.creatures, k=min(3, total_creatures))
        sample_info = [c.info() for c in sample_creatures]

        return {
            "current_cycle": self.current_cycle,
            "total_creatures": total_creatures,
            "strategy_counts": dict(strategy_counts),
            "sample_creatures": sample_info
        }

