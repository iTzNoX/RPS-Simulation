from Creature import Creature
from collections import Counter
import random

class Simulation:
    """
    Represents a single Simulation with multiple Cycles. One Cycle can be seen as one day.
    Handles everything regarding the Simulation
    """
    id_counter = 0

    def __init__(self, participants: int = 9999, max_cycles: int = 10, distribution: list[int] = None):
        """
        Initializes a Simulation instance.

        Attributes:
            Configuration:
                participants (int): Total number of participants (rounded downwards to nearest multiple of 3).
                max_cycles (int): Number of max simulation cycles to run.
                distribution (list[int]): Exact number of participants per strategy [R, P, S].
                strategies (list[str]): Ordered list of available strategies.
            runtime state:
                creatures (list[Creature]): List of all Creature objects participating in the simulation.
                current_cycle (int): Index of the currently processed simulation cycle.
                current_participants (int): Current number of living creatures.
        """
        self.id = f"{Simulation.id_counter:06d}"
        Simulation.id_counter += 1

        self.max_cycles = max_cycles
        self.participants = participants - (participants % 3)

        self.current_cycle = 0
        self.current_participants = self.participants

        if distribution is None:
            per_strategy = self.participants // 3
            self.distribution = [per_strategy] * 3
        else:
            if len(distribution) != 3:
                raise ValueError("Distribution must have exactly 3 int values, representing the amount of (R, P, S).")
            if not all(isinstance(x, int) and x >= 0 for x in distribution):
                raise ValueError("Distribution values must be non-negative integers.")
            if sum(distribution) != self.participants:
                raise ValueError(
                    f"Sum of distribution ({sum(distribution)}) must equal total participants "
                    f"({self.participants}, rounded down to nearest multiple of 3)."
                )
            self.distribution = distribution

        self.creatures = []
        self.strategies = ["R", "P", "S"]
        for strategy, count in zip(self.strategies, self.distribution):
            for _ in range(count):
                self.creatures.append(Creature(strategy=strategy))

    def next_cycle(self):

        creature_pool = self.creatures[:]
        already_played = []
        offspring_list = []

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

    def info(self) -> dict:
        """
        Returns a snapshot of the current simulation state.

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

