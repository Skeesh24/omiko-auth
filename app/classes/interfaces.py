from abc import ABC, abstractclassmethod
from typing import Any, Union


class ICacheService(ABC):
    @abstractclassmethod
    def get(self, key: str) -> str:
        pass

    @abstractclassmethod
    def set(self, key: str, value: str) -> bool:
        pass

    @abstractclassmethod
    def elem_and_status(self, key: str) -> Union[str, bool]:
        pass

    @abstractclassmethod
    def remove(self, key: str) -> bool:
        pass

    @abstractclassmethod
    def close(self) -> None:
        pass
