from World import World

def main():
    """
    Main entry point for running the Rock-Paper-Scissors Simulation.

    This script initializes a World instance with a specified number of participants
    and maximum cycles. It then runs the simulation day by day (cycle by cycle), printing
    a structured summary of the World state after each cycle, including:

    - Current cycle index
    - Total number of living creatures
    - Count of creatures per strategy (R, P, S)
    - Sample details of 3 random creatures, including their ID, strategy, and generation

    At the end of the simulation, a final summary is printed, showing the final cycle,
    total remaining creatures, and the final strategy counts.

    Notes:
    - The World ends either when the maximum number of cycles is reached or when
      there are no more living creatures.
    - The `World` and `Creature` classes handle all internal mechanics, such as
      interactions, reproduction, and ID management.
    - The higher the participants are the longer the cycles will take. it's recommended to stay under 1 Million
      participants.
    """
    sim = World(start_participants=9999, max_cycles=100)

    print("Starting simulation...\n")

    while sim.current_cycle < sim.max_cycles and sim.current_participants > 0:
        sim.next_cycle()
        info = sim.info()

        print(f"Cycle {info['current_cycle']}:")
        print(f"  Total Creatures: {info['total_creatures']}")
        print(f"  Strategy Counts:")
        for strategy, count in info['strategy_counts'].items():
            print(f"    {strategy}: {count}")

        print(f"  Sample Creatures:")
        for c in info['sample_creatures']:
            print(f"    ID: {c['id']}")
            print(f"      Strategy: {c['strategy']}")
            print(f"      Generation: {c['generation']}")
        print("-" * 40)

    print("\nSimulation ended.")
    final_info = sim.info()
    print(f"Final cycle: {final_info['current_cycle']}")
    print(f"Total creatures: {final_info['total_creatures']}")
    print("Final strategy counts:")
    for strategy, count in final_info['strategy_counts'].items():
        print(f" {strategy}: {count}")

if __name__ == "__main__":
    main()
