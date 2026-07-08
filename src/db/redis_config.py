from redis.asyncio import Redis
import asyncio
from src.config import settings

JTI_EXPIRY = 3600

token_blocklist = Redis.from_url(
    url=settings.REDIS_URL
)

async def add_JTI_to_Blocklist(jti: str):
    await token_blocklist.set(jti, "", ex=JTI_EXPIRY)

async def CHECK_JTI_IN_BLOCKLIST(jti: str):
    jti_ = await token_blocklist.get(jti)
    return jti_ is not None