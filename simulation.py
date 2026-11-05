from dataclasses import dataclass
import statistics

from reward import RewardType
from mission import Mission


@dataclass
class TrialResult:
    trial: int
    total_rewards: dict[RewardType, float]
    total_time: float
    missions_completed: int
    repetitions_done: int


@dataclass
class StrategySummary:
    strategy: int
    trials: int
    average_time: float
    std_dev_time: float
    min_time: float
    max_time: float
    average_missions: float
    average_repetitions: float
    extra_rewards: dict[RewardType, float]


class Simulation:
    def __init__(self,
        mission: Mission,
        trials: int,
        mission_rounds: int,
        reward_goal: dict[RewardType, float],
        verbose: bool = False,
    ) -> None:
        self.mission = mission
        self.trials = trials
        self.mission_rounds = mission_rounds
        self.reward_goal = reward_goal
        self.verbose = verbose


    def run_simulation(self) -> list[TrialResult]:
        if not self.reward_goal:
            raise RuntimeError("Empty Reward goal list")

        for key, value in self.reward_goal.items():
            if value <= 0:
                raise RuntimeError("Goal amount less than or 0 for: " + str(key))

        results: list[TrialResult] = []
        MAX_RUNS = 1000

        for i in range(self.trials):
            if self.verbose:
                print("Trial: " + str(i))

            total_rewards: dict[RewardType, float] = {}
            total_time = 0.0
            missions_completed = 0
            total_repetitions = 0

            while True:
                if missions_completed >= MAX_RUNS:
                    raise RuntimeError("Max runs exceeded for trial" + str(i))

                cycle_rewards, cycle_time, cycle_repetitions = self.run_mission()

                for key, value in cycle_rewards.items():
                    total_rewards[key] = total_rewards.get(key, 0.0) + value

                total_time += cycle_time
                total_repetitions += cycle_repetitions
                missions_completed += 1

                if self.check_reward_goal(total_rewards):
                    results.append(
                        TrialResult(
                            trial=i,
                            total_rewards=total_rewards.copy(),
                            total_time=total_time,
                            missions_completed=missions_completed,
                            repetitions_done=total_repetitions,
                        )
                    )
                    break

                total_time += self.mission.get_reset_time()

        return results


    def summarize_results(self, trial_results: list[TrialResult]) -> StrategySummary:
        if not trial_results:
            raise RuntimeError("No trial results available to summarize.")

        total_times: list[float] = []
        missions_completed: list[int] = []
        repetitions_done: list[int] = []
        extra_reward_history: dict[RewardType, list[float]] = {}

        for reward_type in self.reward_goal.keys():
            extra_reward_history[reward_type] = []

        for result in trial_results:
            total_times.append(float(result.total_time))
            missions_completed.append(int(result.missions_completed))
            repetitions_done.append(int(result.repetitions_done))

            total_reward = result.total_rewards

            for reward_type, goal_amount in self.reward_goal.items():
                extra_reward_history[reward_type].append(
                    max(0.0, total_reward[reward_type] - goal_amount)
                )


        extra_rewards = {}

        for reward_type, values in extra_reward_history.items():
            if values:
                extra_rewards[reward_type] = statistics.mean(values)

        return StrategySummary(
            strategy=self.mission_rounds,
            trials=len(trial_results),
            average_time=statistics.mean(total_times),
            std_dev_time=statistics.pstdev(total_times) if len(total_times) > 1 else 0.0,
            min_time=min(total_times),
            max_time=max(total_times),
            average_missions=statistics.mean(missions_completed),
            average_repetitions=statistics.mean(repetitions_done),
            extra_rewards=extra_rewards,
        )


    def check_reward_goal(self, curr_rewards: dict[RewardType, float]) -> bool:
        for reward_type, amount in self.reward_goal.items():
            if reward_type not in curr_rewards:
                return False
            if curr_rewards[reward_type] < amount:
                return False
        return True


    def run_mission(self) -> tuple[dict[RewardType, float], float, int]:
        cycle_rewards: dict[RewardType, float] = {}
        cycle_time = 0.0
        repetitions = 0

        for round_number in range(1, self.mission_rounds + 1):
            rewards = self.mission.get_rewards(round_number)
            completion_time = self.mission.get_completion_time(round_number)
            menu_time = self.mission.get_menu_time(round_number)

            for key, value in rewards.items():
                cycle_rewards[key] = cycle_rewards.get(key, 0.0) + value

            cycle_time += completion_time
            cycle_time += menu_time
            repetitions += 1

        return cycle_rewards, cycle_time, repetitions
