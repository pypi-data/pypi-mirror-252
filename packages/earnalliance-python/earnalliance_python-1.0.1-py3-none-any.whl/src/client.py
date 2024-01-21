from typing import Any, Dict, Optional
from options import NodeOptions
from model.execution_result import ExecutionResult
from model.identifier_prop_names import IdentifierPropNames
from model.queue_item import Identifier
from transporter.http_transporter import HTTPTransporter
from processor.batch_processor import BatchProcessor
from utils import track, track_with_value, track_with_traits, identify
from model.round import Round
from model.identifying_properties import IdentifyingProperties


class NodeClient:
    def __init__(self, options: NodeOptions):
        self.transporter = HTTPTransporter(options)
        self.options = options
        self.processor = BatchProcessor(self.transporter, options)

    async def start_game(self, user_id: str) -> ExecutionResult:
        """Starts a game and adds the event to the processor."""
        event = track(user_id, "START_GAME")
        return await self.processor.add_event(event)

    def start_round(self, group_id: Optional[str] = None) -> Round:
        """Starts a new round."""
        return Round(self.processor, group_id)

    async def track(
        self,
        user_id: str,
        event_name: str,
    ) -> ExecutionResult:
        """Tracks an event and adds it to the processor."""
        event = track(user_id, event_name)
        return await self.processor.add_event(event)

    async def track_with_traits(
        self,
        user_id: str,
        event_name: str,
        *traits: Dict[str, Any],
    ) -> ExecutionResult:
        """Tracks an event with specific traits and adds it to the processor."""
        event = track_with_traits(user_id, event_name, *traits)
        return await self.processor.add_event(event)

    async def track_with_value(
        self, user_id: str, event_name: str, value: int
    ) -> ExecutionResult:
        """Tracks an event with specific value and adds it to the processor."""
        event = track_with_value(user_id, event_name, value)
        return await self.processor.add_event(event)

    async def flush(self) -> ExecutionResult:
        """Flushes the processor."""
        return await self.processor.flush()

    async def set_user_identifiers(
        self, user_id: str, identifying_properties: IdentifyingProperties
    ) -> ExecutionResult:
        """Sets user identifiers and adds them to the processor."""
        identifier = identify(user_id, identifying_properties)
        return await self.processor.add_identifier(identifier)

    async def remove_identifiers(
        self, identifier: Identifier, *property_names: IdentifierPropNames
    ) -> ExecutionResult:
        """Removes user identifiers and adds the action to the processor."""
        return await self.processor.add_identifier(identifier.clear(*property_names))
