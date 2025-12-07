import json

from redis.asyncio import Redis
from typing import Optional
from app.utils.config import config

redis: Optional[Redis] = None

async def init_redis():
    global redis
    redis = Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        decode_responses=True
    )

async def get_cache(key: str, model_cls):
    if redis:
        cached = await redis.get(key)
        if cached:
            return model_cls.model_validate_json(cached)
    return None

async def set_cache(key: str, data, time: int = 600):
    if redis:
        await redis.setex(
            key,
            time,
            data.model_dump_json()
        )
