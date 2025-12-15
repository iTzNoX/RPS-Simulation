from Creature import Creature

class Simulation:
    id_counter = 0

    def __init__(self, participants: int = 9999, cycles: int = 10, distribution: list[int] = None):
        Simulation.increase_id_counter()
        self.id = f"{Simulation.id_counter:06d}"

        self.cycles = cycles
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

    @staticmethod
    def increase_id_counter():
        if Simulation.id_counter > 999999:
            raise ValueError("Simulation ID limit reached")
        Simulation.id_counter += 1
