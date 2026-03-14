import redis.asyncio as redis

from src.config import config as c


redis_pool = redis.ConnectionPool(
    db=c.REDIS_DB,
    host=c.REDIS_HOST,
    port=c.REDIS_PORT,
    decode_responses=True,
    max_connections=50
)

redis_client = redis.Redis(connection_pool=redis_pool)
