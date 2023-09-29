from abc import ABC, abstractclassmethod
from typing import Any, Union


class IRepository(ABC):
    @abstractclassmethod
    def get(self, limit: int = 5, offset: int = 0, **kwargs) -> Union[list, Any]:
        pass

    def add(self, element) -> Any:
        pass

    def update(self, element) -> Any:
        pass

    def remove(self, element) -> None:
        pass


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


class IBroker(ABC):
    @abstractclassmethod
    def create_connection(self, host_name: str, queue_name: str) -> None:
        pass

    def publish(self, message: str) -> None:
        pass

    def close(self) -> None:
        pass
