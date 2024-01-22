from abc import ABC, abstractmethod


class DBUtil(ABC):

    @abstractmethod
    async def get_strategy_params(self, acc_id: int, code: str, strategy_id: int) -> dict:
        pass

    @abstractmethod
    async def update_addnew_strategy_params(self, acc_id: int, code: str, strategy_id: int, params: dict):
        pass
