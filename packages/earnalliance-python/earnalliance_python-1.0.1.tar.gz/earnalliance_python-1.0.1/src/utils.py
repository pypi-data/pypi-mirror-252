import asyncio
from typing import Any, Awaitable, Dict, Callable, TypeVar
from model.queue_item import Identifier, Event
from model.identifying_properties import IdentifyingProperties
from datetime import datetime, timezone


def identify(user_id: str, properties: IdentifyingProperties) -> Identifier:
    """Creates and Identifier using the speicifide IdentifyingProperties and user_id"""
    return Identifier(
        userId=user_id,
        appleId=properties.appleId,
        discordId=properties.discordId,
        email=properties.email,
        epicGamesId=properties.epicGamesId,
        steamId=properties.steamId,
        twitterId=properties.twitterId,
        walletAddress=properties.walletAddress,
    )


def track(user_id: str, event_name: str) -> Event:
    """Creates an event for the specified user id and event name"""
    time = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return Event(userId=user_id, time=time, event=event_name)


def track_with_value(user_id: str, event_name: str, value: int) -> Event:
    """Creates an event for the specified user id event name, including numeric value as value field and trait"""
    event = track(user_id, event_name)
    event.value = value
    return event


def track_with_traits(user_id: str, event_name: str, *traits: Dict[str, Any]) -> Event:
    """Creates an event for the specified user id, event name together with the specified traits dictionary"""
    event = track(user_id, event_name)
    event.traits = list(traits)
    return event


class Scheduler:
    T = TypeVar("T")

    @staticmethod
    async def delay(callback: Callable[[], Awaitable[T]], delay_seconds: int) -> T:
        await asyncio.sleep(delay_seconds)
        return await callback()
