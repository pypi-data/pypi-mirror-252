import uuid
from asyncio import Future
from typing import Any, Dict, Optional

from utils import track_with_traits, track_with_value, track

from model.execution_result import ExecutionResult
from model.queue_item import Event
from processor.batch_processor import BatchProcessor


class Round:
    def __init__(self, processor: BatchProcessor, group_id: Optional[str]) -> None:
        self.group_id = group_id if group_id is not None else str(uuid.uuid4())
        self.processor = processor

    async def track(
        self,
        user_id: str,
        event_name: str,
    ) -> ExecutionResult:
        """Tracks an event and adds it to the processor."""
        event = track(user_id, event_name)
        return await self.add_event(event)

    async def track_with_traits(
        self,
        user_id: str,
        event_name: str,
        *traits: Dict[str, Any],
    ) -> ExecutionResult:
        """Tracks an event with specific traits and adds it to the processor."""
        event = track_with_traits(user_id, event_name, *traits)
        return await self.add_event(event)

    async def track_with_value(
        self, user_id: str, event_name: str, value: int
    ) -> ExecutionResult:
        """Tracks an event with specific value and adds it to the processor."""
        event = track_with_value(user_id, event_name, value)
        return await self.add_event(event)

    def add_event(self, event: Event) -> Future[ExecutionResult]:
        event.groupId = self.group_id
        return self.processor.add_event(event)
