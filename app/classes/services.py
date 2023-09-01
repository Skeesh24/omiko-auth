from typing import Union

from configuration import Settings
from classes.interfaces import ICacheService
from memcache import Client


class MemcachedService(ICacheService):
    def __init__(self, hosts) -> None:
        self.client = Client(hosts)

    def get(self, key: str) -> str:
        return self.client.get(key)

    def set(self, key: str, value: str):
        return self.client.set(key, value)

    def elem_and_status(self, key: str) -> (Union[str, int], bool):
        value = self.get(key)
        if value is None or value == 0:
            return (None, False)
        return (value, True)

    def remove(self, key: str) -> bool:
        return self.client.delete(key)

    def close(self) -> None:
        try:
            self.client.disconnect_all()
        except Exception as e:
            # add logging
            print("Error closing memcached session: " + str(e))
        finally:
            # ?
            # del self.client
            ...


SettingsService = Settings()
