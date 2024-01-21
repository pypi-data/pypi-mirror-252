from typing import Any, Dict, List
from model.identifier_prop_names import IdentifierPropNames


class QueueItem:
    pass


class Identifier(QueueItem):
    def __init__(
        self,
        userId,
        appleId,
        discordId,
        email,
        epicGamesId,
        steamId,
        twitterId,
        walletAddress,
    ) -> None:
        self.userId = userId
        self.appleId = appleId
        self.discordId = discordId
        self.email = email
        self.epicGamesId = epicGamesId
        self.steamId = steamId
        self.twitterId = twitterId
        self.walletAddress = walletAddress

    def __json__(self):
        return {
            "userId": self.userId,
            "appleId": self.appleId,
            "discordId": self.discordId,
            "email": self.email,
            "epicGamesId": self.epicGamesId,
            "steamId": self.steamId,
            "twitterId": self.twitterId,
            "walletAddress": self.walletAddress,
        }

    def __eq__(self, value) -> bool:
        if not isinstance(value, Identifier):
            return False

        return (
            self.userId == value.userId
            and self.appleId == value.appleId
            and self.discordId == value.discordId
            and self.email == value.email
            and self.epicGamesId == value.epicGamesId
            and self.steamId == value.steamId
            and self.twitterId == value.twitterId
            and self.walletAddress == value.walletAddress
        )

    def clear(self, *property_names: IdentifierPropNames):
        for prop in property_names:
            setattr(self, prop.value, None)

        return self


class Event(QueueItem):
    def __init__(
        self,
        userId,
        time,
        event,
        traits: List[Dict[str, Any]] = [],
        groupId=None,
        value=None,
    ) -> None:
        self.userId = userId
        self.time = time
        self.event = event
        self.groupId = groupId
        self.traits = traits
        self.value = value

    def __json__(self):
        result = {
            "userId": self.userId,
            "time": self.time,
            "event": self.event,
        }

        if self.traits:
            result["traits"] = self.traits

        if self.groupId is not None:
            result["groupId"] = self.groupId

        if self.value is not None:
            result["value"] = self.value

        return result
