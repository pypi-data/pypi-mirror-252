from typing import List

from validation import required
from constants import DEFAULT_INTERVAL, DEFAULT_MAX_RETRY_ATTEMPTS, DEFAULT_BATCH_SIZE


@required("clientId", "clientSecret", "dsn", "gameId")
class NodeOptions:
    def __init__(
        self,
        dsn: str,
        gameId: str,
        clientId: str,
        clientSecret: str,
        flushEvents: List[str] = [],
        interval: int = DEFAULT_INTERVAL,
        maxRetryAttempts: int = DEFAULT_MAX_RETRY_ATTEMPTS,
        batchSize: int = DEFAULT_BATCH_SIZE,
    ):
        self.batchSize = batchSize
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.dsn = dsn
        self.flushEvents = flushEvents
        self.gameId = gameId
        self.interval = interval
        self.maxRetryAttempts = maxRetryAttempts
