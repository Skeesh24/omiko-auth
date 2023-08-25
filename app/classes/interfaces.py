from abc import ABC, abstractclassmethod
from typing import Any, Union


class ICacheService(ABC):
    @abstractclassmethod
    def get(self, key: str) -> tuple[int, str, None]:
        pass

    @abstractclassmethod
    def set(self, key: str, value: str) -> Any | bool:
        pass

    @abstractclassmethod
    def elem_and_status(self, key: str) -> Union[tuple[int, str, None], bool]:
        pass

    @abstractclassmethod
    def remove(self, key: str) -> bool:
        pass

    @abstractclassmethod
    def close(self) -> None:
        pass
