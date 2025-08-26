import redis.asyncio as redis
import logging


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        logging.info(f"Идет подключение к Redis host={self.host}, port={self.port}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Подключение успешно установлено к Redis host={self.host}, port={self.port}")

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        return await self.redis.get(key)

    async def delete(self, key: str):
        await self.redis.delete(key)
