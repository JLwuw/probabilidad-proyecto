from reward import RewardType
from mission import Mission

class Simulation:
    def __init__(self,
        mission: Mission,
        trials: int,
        mission_rounds: int,
        reward_goal: dict[RewardType, float]
    ) -> None:
        self.mission = mission
        self.trials = trials
        self.mission_rounds = mission_rounds
        self.reward_goal = reward_goal
            

    def run_simulation(self) -> list[tuple[dict[RewardType, float], int]]:
        if not self.reward_goal:
            raise RuntimeError("Empty Reward goal list")

        for key, value in self.reward_goal.items():
            if value <= 0:
                raise RuntimeError("Goal amount less than or 0 for: " + str(key))

        results = []
        MAX_RUNS = 1000

        for i in range(self.trials):
            print("Trial: " + str(i))

            total_rewards = {}
            total_time = 0
            run = 1

            while True:
                if run > MAX_RUNS:
                    raise RuntimeError("Max runs exceeded. Skipping trial: " + str(i))

                completion_time = self.mission.get_completion_time(self.mission_rounds)
                rewards = self.mission.get_rewards(self.mission_rounds)
                
                for key, value in rewards.items():
                    total_rewards[key] = total_rewards.get(key, 0) + value

                total_time += completion_time
                total_time += self.mission.get_menu_time(self.mission_rounds)

                if self.check_reward_goal(total_rewards):
                    results.append((total_rewards.copy(), total_time))
                    break

                run += 1

        return results
                

    def check_reward_goal(self, curr_rewards: dict[RewardType, float] ) -> bool:
        for reward_type, amount in self.reward_goal.items():
            if reward_type not in curr_rewards:
                return False
            if curr_rewards[reward_type] < amount:
                return False
        return True


    def run_mission(self) -> tuple[dict[RewardType, float], int]:
        rewards = self.mission.get_rewards(self.mission_rounds)
        completion_time = self.mission.get_completion_time(self.mission_rounds)

        return rewards, completion_time
