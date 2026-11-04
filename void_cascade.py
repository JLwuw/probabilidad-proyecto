from mission import Mission
from reward import RewardType, MissionReward
import numpy as np


class VoidCascade(Mission):
    def __init__(self, rng) -> None:
        self.rng = rng


    def get_menu_time(self, round: int) -> int:
        return (20 * round) + 30


    def get_completion_time(self, round: int) -> int:
        if round not in VOID_CASCADE_REPETITION_TIMES:
            raise RuntimeError("undefined average round time: " + str(round))

        return VOID_CASCADE_REPETITION_TIMES[round]
    

    def get_rewards(self, round: int) -> dict[RewardType, float]:
        mission_rewards = self.get_mission_rewards(round)
        rewards = mission_rewards.copy()
        
        enemy_drops = self.get_enemy_drops(round)
        for key, value in enemy_drops.items():
            rewards[key] = rewards.get(key, 0) + value

        relic_rewards = self.get_void_relic_reward(round)
        for key, value in relic_rewards.items():
            rewards[key] = rewards.get(key, 0) + value
        
        return rewards


    def get_void_relic_reward(self, round: int) -> dict[RewardType, float]:
        reward_types = (
            RewardType.COMMON_VOID_RELIC_REWARD,
            RewardType.UNCOMMON_VOID_RELIC_REWARD,
            RewardType.RARE_VOID_RELIC_REWARD,
        )
        rewards = {}
        for _ in range(round):
            index = self.rng.choice(len(reward_types), p=[0.76, 0.22, 0.02])
            reward_type = reward_types[index]
            rewards[reward_type] = rewards.get(reward_type, 0.0) + 1.0
        return rewards


    def get_mission_rewards(self, round: int) -> dict[RewardType, float]:
        total_rewards = {}

        for i in range(round):
            rotation_idx = i % len(VOID_CASCADE_ROTATION)
            rotation = VOID_CASCADE_ROTATION[rotation_idx]

            if rotation not in VOID_CASCADE_DROP_TABLES:
                raise RuntimeError("No drop table defined for rotation: " + rotation)

            table = VOID_CASCADE_DROP_TABLES[rotation]

            probabilities = np.array(
                [reward.probability for reward in table]
            )

            probabilities /= probabilities.sum()
            index = self.rng.choice(len(table), p=probabilities)
            chosen_reward = table[index]

            total_rewards[chosen_reward.type] = total_rewards.get(chosen_reward.type, 0) + chosen_reward.quantity

        return total_rewards


    def get_enemy_drops(self, round: int) -> dict[RewardType, float]:
        if round not in VOID_CASCADE_EXPECTED_ENEMY_DROPS:
            raise RuntimeError("undefined enemy drops for repetition: " + str(round))

        return VOID_CASCADE_EXPECTED_ENEMY_DROPS[round]

        

# void cascade goes AABC AABC ...
VOID_CASCADE_ROTATION = ['A', 'A', 'B', 'C']


# key: rotation
# value: drop table
VOID_CASCADE_DROP_TABLES = {
    'A': [
        MissionReward(RewardType.CREDITS, 5000, 50.00),
        MissionReward(RewardType.ENDO, 450, 18.75),
        MissionReward(RewardType.VOIDGEL_ORB, 1, 9.38),
        MissionReward(RewardType.MESO_RELIC, 1, 21.87),
    ],

    'B': [
        MissionReward(RewardType.CREDITS, 7500, 50.00),
        MissionReward(RewardType.ENDO, 600, 20.00),
        MissionReward(RewardType.ENTRATI_LANTHORN, 1, 6.67),
        MissionReward(RewardType.NEO_RELIC, 1, 23.31),
    ],

    'C': [
        MissionReward(RewardType.LENS, 1, 80.00),
        MissionReward(RewardType.AEOLAK_BARREL_BLUEPRINT, 1, 10.00),
        MissionReward(RewardType.HESPAR_HANDLE_BLUEPRINT, 1, 10.00),
    ]
}

# Key: round
# Value: seconds to finish round
VOID_CASCADE_REPETITION_TIMES = {
    1: 265,
    2: 511,
    3: 775, 
    4: 1152,
    5: 1628,
    6: 2142,
    7: 2919,
    8: 3781,
}

# Key: round
# Value: dict of drops
VOID_CASCADE_EXPECTED_ENEMY_DROPS = {
    1: {
        RewardType.VOIDGEL_ORB: 12,
        RewardType.THRAX_PLASM: 71.66666667,
        RewardType.ARCANE: 0.6666666667,
    },
    2: {
        RewardType.VOIDGEL_ORB: 25,
        RewardType.THRAX_PLASM: 112.3333333,
        RewardType.ARCANE: 1.333333333,
    },
    3: {
        RewardType.VOIDGEL_ORB: 33,
        RewardType.THRAX_PLASM: 150,
        RewardType.ARCANE: 1.666666667,
    },
    4: {
        RewardType.VOIDGEL_ORB: 48.66666667,
        RewardType.THRAX_PLASM: 237,
        RewardType.ARCANE: 2.666666667,
    },
    5: {
        RewardType.VOIDGEL_ORB: 59.33333333,
        RewardType.THRAX_PLASM: 356.3333333,
        RewardType.ARCANE: 3,
    },
    6: {
        RewardType.VOIDGEL_ORB: 71,
        RewardType.THRAX_PLASM: 440.3333333,
        RewardType.ARCANE: 3.333333333,
    },
    7: {
        RewardType.VOIDGEL_ORB: 84.66666667,
        RewardType.THRAX_PLASM: 550.6666667,
        RewardType.ARCANE: 3.666666667,
    },
    8: {
        RewardType.VOIDGEL_ORB: 101.6666667,
        RewardType.THRAX_PLASM: 653,
        RewardType.ARCANE: 4.333333333,
    },
}
