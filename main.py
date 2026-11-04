from __future__ import annotations

import numpy as np

from reward import RewardType
from simulation import Simulation, StrategySummary
from void_cascade import VoidCascade


RNG_SEED = 49
REWARD_GOAL = {
    RewardType.VOIDGEL_ORB: 250,
    RewardType.THRAX_PLASM: 1500,
    RewardType.ARCANE: 8,
}
TRIALS_PER_STRATEGY = 25
STRATEGIES = [1, 2, 3, 4, 5, 6, 7, 8]


def run_strategy(strategy: int) -> StrategySummary:
    rng = np.random.default_rng(RNG_SEED + strategy)
    mission = VoidCascade(rng)
    simulation = Simulation(
        mission=mission,
        trials=TRIALS_PER_STRATEGY,
        mission_rounds=strategy,
        reward_goal=REWARD_GOAL,
    )

    results = simulation.run_simulation()
    summary = simulation.summarize_results(results)
    return summary


def print_summary_table(rows: list[StrategySummary]) -> None:
    print("\nSimulation results ordered by average completion time")
    print("-" * 120)
    print(
        f"{'Strategy':>8} | {'Avg time (s)':>14} | {'Stddev':>10} | {'Min':>10} | {'Max':>10} | "
        f"{'Avg missions':>14} | {'Avg repetitions':>16}"
    )
    print("-" * 120)

    for row in rows:
        print(
            f"{row.strategy:>8} | {row.average_time:>14.1f} | {row.std_dev_time:>10.1f} | {row.min_time:>10.1f} | {row.max_time:>10.1f} | "
            f"{row.average_missions:>14.1f} | {row.average_repetitions:>16.1f}"
        )

    print("-" * 120)


def print_extra_reward_table(rows: list[StrategySummary]) -> None:
    reward_types = sorted(
        {reward for row in rows for reward in row.extra_rewards.keys()},
        key=lambda reward: reward.name,
    )

    print("\nAverage extra rewards by item")
    print("-" * 120)
    print(f"{'Strategy':>8} | {'Reward type':>28} | {'Avg extra':>12}")
    print("-" * 120)

    for row in rows:
        for reward_type in reward_types:
            extra = row.extra_rewards.get(reward_type, 0.0)
            print(f"{row.strategy:>8} | {reward_type.name:>28} | {extra:>12.2f}")

    print("-" * 120)


def main() -> None:
    print(f"RNG seed: {RNG_SEED}")
    print(f"Reward goal: {REWARD_GOAL}")
    print(f"Strategies tested: {STRATEGIES}")
    print(f"Trials per strategy: {TRIALS_PER_STRATEGY}")

    rows = [run_strategy(strategy) for strategy in STRATEGIES]
    rows.sort(key=lambda row: row.average_time)
    print_summary_table(rows)
    print_extra_reward_table(rows)


if __name__ == "__main__":
    main()
