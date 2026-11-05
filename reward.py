from enum import Enum, auto
from dataclasses import dataclass


class RewardType(Enum):
    CREDITS = auto()
    ENDO = auto()
    VOIDGEL_ORB = auto()
    ENTRATI_LANTHORN = auto()
    THRAX_PLASM = auto()
    ARCANE = auto()

    MESO_RELIC = auto()
    NEO_RELIC = auto()

    LENS = auto()

    AEOLAK_BARREL_BLUEPRINT = auto()
    HESPAR_HANDLE_BLUEPRINT = auto()

    COMMON_VOID_RELIC_REWARD = auto()
    UNCOMMON_VOID_RELIC_REWARD = auto()
    RARE_VOID_RELIC_REWARD = auto()

    NARIN_NEUROPTICS_BLUEPRINT = auto()


@dataclass(frozen=True)
class MissionReward:
    type: RewardType
    quantity: float = 1.0
    probability: float = 0.0

