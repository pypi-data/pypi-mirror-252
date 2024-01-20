import os
from abc import abstractmethod
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum
from typing import Dict, Optional

from redis import ConnectionPool, Redis
from redis.exceptions import ConnectionError

ENABLE_RATE_LIMIT = os.getenv("ENABLE_RATE_LIMIT", "True") == "True"

MAX_RETRY = 1


class RateLimitException(Exception):
    rate_id: str

    def __init__(
        self,
        rate_id: str,
        rate_limit: Optional[float],
        rate: Optional[int],
        hint: str = "",
    ):
        if hint:
            hint = " Hint :: " + hint
        super().__init__(
            f"Usage rate :: {rate} exceeds rate_limit :: {rate_limit} with rate_id :: {rate_id}.{hint}"  # noqa
        )
        self.rate_id = rate_id


class Tier(Enum):
    FREE = "free"
    PRO = "pro"
    MANAGED = "managed"


@dataclass
class UserRate:
    user_rate: int
    tier: Tier
    tier_limits: Dict[Tier, float]


UNLIMITED = float("inf")


class Counter:
    _redis_client: Redis

    def __init__(
        self,
        redis_host: str,
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
    ):
        self.redis_host = redis_host
        self.redis_port = redis_port
        self.redis_password = redis_password

    @property
    def redis_client(self) -> Redis:
        if not hasattr(self, "_redis_client"):
            redis_pool = ConnectionPool(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
            )
            self._redis_client = Redis(
                connection_pool=redis_pool, health_check_interval=30
            )
        return self._redis_client

    def incr(
        self,
        key: str,
        timedelta_: timedelta,
        retry: int = 0,
    ) -> None:
        try:
            if self.redis_client.exists(key):
                self.redis_client.incr(key)
            else:
                self.redis_client.set(key, 1, ex=timedelta_)
        except ConnectionError as e:
            if retry >= MAX_RETRY:
                raise e
            self.incr(key, timedelta_, retry=retry + 1)

    def get(self, key: str, retry: int = 0) -> int:
        try:
            return int(self.redis_client.get(key) or 0)
        except ConnectionError as e:
            if retry < MAX_RETRY:
                return self.get(key, retry=retry + 1)
            raise e


class ValidateRateLimitRedis:
    def __init__(
        self,
        rate_id: str,
        tier_limits: Dict[Tier, float],
        timedelta_: timedelta,
        redis_host: str,
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
    ):
        assert (
            Tier.FREE in tier_limits and Tier.PRO in tier_limits
        ), f"ValidateRateLimit.tier_limits must declare rate limits for :: {Tier.FREE} and {Tier.PRO}"  # noqa

        self.rate_id = rate_id
        self.timedelta_ = timedelta_
        self.counter = Counter(redis_host, redis_port, redis_password)

        # Set special tier limits
        self.tier_limits = tier_limits
        self.tier_limits[Tier.MANAGED] = UNLIMITED

    def validate_user_rate(self, user_id: str) -> None:
        if not ENABLE_RATE_LIMIT:
            return

        key = self.key(user_id)

        # Get user data
        user_tier = self.get_user_tier(user_id)
        user_rate = self.counter.get(key)

        # Check rate limit
        rate_limit = self.tier_limits.get(user_tier, -1)
        if user_rate >= rate_limit:
            raise RateLimitException(self.rate_id, rate_limit, user_rate)

        # Update user rate
        self.counter.incr(key, self.timedelta_)

    def key(self, user_id: str) -> str:
        return f"{user_id}/{self.rate_id}"

    def get_user_rate(self, user_id: str) -> UserRate:
        # Tier limits
        tier_limits = {**self.tier_limits}  # copy
        tier_limits[Tier.MANAGED] = -1

        key = self.key(user_id)
        return UserRate(
            user_rate=self.counter.get(key),
            tier=self.get_user_tier(user_id),
            tier_limits=tier_limits,
        )

    @abstractmethod
    def get_user_tier(self, user_id: str) -> Tier:
        ...
