from mission import Mission
from reward import RewardType, MissionReward
import numpy as np


class VoidCascade(Mission):
    def __init__(self, rng) -> None:
        self.rng = rng


    def get_menu_time(self, round: int) -> int:
        return 10


    def get_reset_time(self):
        return 60

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
        index = self.rng.choice(len(reward_types), p=[0.76, 0.22, 0.02])
        reward_type = reward_types[index]
        return {reward_type: 1.0}


    def get_mission_rewards(self, round: int) -> dict[RewardType, float]:
        rotation_idx = round % len(VOID_CASCADE_ROTATION)
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

        return {chosen_reward.type: chosen_reward.quantity}


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
    2: 246,
    3: 529,
    4: 623,
    5: 1005,
    6: 1137,
    7: 1782,
    8: 1999,
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
        RewardType.VOIDGEL_ORB: 13,
        RewardType.THRAX_PLASM: 54,
        RewardType.ARCANE: 0.6666666667,
    },
    3: {
        RewardType.VOIDGEL_ORB: 8,
        RewardType.THRAX_PLASM: 44.33333333,
        RewardType.ARCANE: 0.3333333333,
    },
    4: {
        RewardType.VOIDGEL_ORB: 15.66666667,
        RewardType.THRAX_PLASM: 67,
        RewardType.ARCANE: 0.6666666667,
    },
    5: {
        RewardType.VOIDGEL_ORB: 14,
        RewardType.THRAX_PLASM: 119.3333333,
        RewardType.ARCANE: 0.3333333333,
    },
    6: {
        RewardType.VOIDGEL_ORB: 15,
        RewardType.THRAX_PLASM: 84,
        RewardType.ARCANE: 0.3333333333,
    },
    7: {
        RewardType.VOIDGEL_ORB: 13.66666667,
        RewardType.THRAX_PLASM: 110.3333333,
        RewardType.ARCANE: 0.3333333333,
    },
    8: {
        RewardType.VOIDGEL_ORB: 17,
        RewardType.THRAX_PLASM: 102.3333333,
        RewardType.ARCANE: 0.6666666667,
    },
}
