from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from mh_logger.mh_rate_limit import (
    ENABLE_RATE_LIMIT,
    UNLIMITED,
    Counter,
    RateLimitException,
    Tier,
)


@dataclass
class UserRate:
    user_rate: int
    tier: Tier
    tier_limits: Dict[Tier, float]
    tier_changed_at: datetime


class ValidateRateLimitRedisV2:
    def __init__(
        self,
        rate_id: str,
        tier_limits: Dict[Tier, float],
        redis_host: str,
        redis_port: int = 6379,
        redis_password: Optional[str] = None,
    ):
        assert (
            Tier.FREE in tier_limits and Tier.PRO in tier_limits
        ), f"ValidateRateLimit.tier_limits must declare rate limits for :: {Tier.FREE} and {Tier.PRO}"  # noqa

        self.rate_id = rate_id
        self.counter = Counter(redis_host, redis_port, redis_password)

        # Set special tier limits
        self.tier_limits = tier_limits
        self.tier_limits[Tier.MANAGED] = UNLIMITED

    def validate_user_rate(self, user_id: str) -> None:
        if not ENABLE_RATE_LIMIT:
            return

        key = self.key(user_id)

        # Get user data
        rate = self.get_user_rate(user_id)

        # Check rate limit
        rate_limit = self.tier_limits.get(rate.tier, -1)
        if rate.user_rate >= rate_limit:
            raise RateLimitException(self.rate_id, rate_limit, rate.user_rate)

        # Update user rate
        timedelta_ = self.calculate_timedelta(rate.tier_changed_at)
        self.counter.incr(key, timedelta_)

    def key(self, user_id: str) -> str:
        return f"{user_id}/{self.rate_id}"

    def get_user_rate(self, user_id: str) -> UserRate:
        # Tier limits
        tier_limits = {**self.tier_limits}  # copy
        tier_limits[Tier.MANAGED] = -1

        user = self.get_user(user_id)
        key = self.key(user_id)

        # Set default to 30 days in the past
        default_tier_changed_at = datetime.now() - timedelta(days=30)
        return UserRate(
            user_rate=self.counter.get(key),
            tier=Tier[user.get("tier", "free")],
            tier_limits=tier_limits,
            tier_changed_at=user.get(
                "tier_updated_at", default_tier_changed_at
            ),
        )

    def calculate_timedelta(self, tier_updated_at: datetime) -> timedelta:
        """
        Calculates how much time in the future to the specified tier_changed_at
        """
        now = datetime.now()
        return (
            datetime(
                year=now.year,
                month=tier_updated_at.month + 1,
                day=tier_updated_at.day,
            )
            - now
        )

    @abstractmethod
    def get_user(self, user_id: str) -> Dict[str, Any]:
        ...
