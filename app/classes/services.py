from typing import Union

from memcache import Client
from redis import Redis

from classes.interfaces import ICacheService
from configuration import Settings


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


class RedisService(ICacheService):
    def __init__(self, url) -> None:
        self.client = Redis.from_url(url)

    def get(self, key: str) -> str:
        return self.client.get(key)

    def set(self, key: str, value: str):
        return self.client.set(key, value)

    def elem_and_status(self, key: str) -> (Union[str, int], bool):
        value = self.get(key)
        if value is None or value == "" or value == 0:
            return (None, False)
        return (value, True)

    def remove(self, key: str) -> bool:
        return self.client.delete(key)

    def close(self) -> None:
        try:
            self.client.close()
        except Exception as e:
            # add logging
            print("Error closing redis session: " + str(e))
        finally:
            # ?
            # del self.client
            ...


SettingsService = Settings()
