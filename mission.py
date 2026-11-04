from abc import ABC, abstractmethod
from reward import RewardType, MissionReward

class Mission(ABC):
    @abstractmethod
    def get_menu_time(self, round: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_completion_time(self, round: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_rewards(self, round: int) -> dict[RewardType, float]:
        raise NotImplementedError