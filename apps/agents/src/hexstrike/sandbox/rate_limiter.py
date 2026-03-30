"""Rate Limiter — Control request rates to avoid overwhelming targets."""

import asyncio
import time
from collections import defaultdict


class RateLimiter:
    """Token bucket rate limiter for controlling scan intensity."""

    def __init__(self, requests_per_second: float = 10.0, burst_size: int = 20):
        self.rate = requests_per_second
        self.burst_size = burst_size
        self._tokens: dict[str, float] = defaultdict(lambda: float(burst_size))
        self._last_refill: dict[str, float] = defaultdict(time.monotonic)
        self._lock = asyncio.Lock()

    async def acquire(self, target: str) -> None:
        """Wait until a request token is available for the target."""
        async with self._lock:
            self._refill(target)
            while self._tokens[target] < 1.0:
                wait_time = (1.0 - self._tokens[target]) / self.rate
                await asyncio.sleep(wait_time)
                self._refill(target)
            self._tokens[target] -= 1.0

    def _refill(self, target: str) -> None:
        now = time.monotonic()
        elapsed = now - self._last_refill[target]
        self._tokens[target] = min(
            self.burst_size, self._tokens[target] + elapsed * self.rate
        )
        self._last_refill[target] = now
