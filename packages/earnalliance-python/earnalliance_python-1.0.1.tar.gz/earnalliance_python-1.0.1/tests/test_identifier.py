from src.model.queue_item import Identifier
from src.model.identifier_prop_names import IdentifierPropNames


def test_clear_identifiers():
    subject = Identifier(
        userId="userId",
        appleId="appleId",
        discordId="discordId",
        email="email",
        epicGamesId="epicGamesId",
        steamId="steamId",
        twitterId="twitterId",
        walletAddress="walletAddress",
    )

    expected = Identifier(
        userId="userId",
        appleId=None,
        discordId="discordId",
        email=None,
        epicGamesId="epicGamesId",
        steamId=None,
        twitterId="twitterId",
        walletAddress="walletAddress",
    )

    actual = subject.clear(
        IdentifierPropNames.APPLE_ID,
        IdentifierPropNames.EMAIL,
        IdentifierPropNames.STEAM_ID,
    )

    assert expected == actual
