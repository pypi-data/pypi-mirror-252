from typing import Dict, List, Any
from model.queue_item import Event, Identifier


class Payload:
    def __init__(
        self, gameId: str, events: List[Event], identifiers: List[Identifier]
    ) -> None:
        self.gameId = gameId
        self.events = events
        self.identifiers = identifiers

    def __json__(self):
        result: Dict[str, Any] = {"gameId": self.gameId}
        events_value = [event.__json__() for event in self.events]
        idents_value = [identifier.__json__() for identifier in self.identifiers]

        result["events"] = events_value
        result.update({"identifiers": idents_value})

        return result
