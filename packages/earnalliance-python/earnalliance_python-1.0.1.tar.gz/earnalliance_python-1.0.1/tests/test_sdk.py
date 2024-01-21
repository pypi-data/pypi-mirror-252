import asyncio
from typing import Any, Dict

from src import client as nc
from src import constants, options, sdk
from src.model.identifier_prop_names import IdentifierPropNames as ipn
from src.model.identifying_properties import IdentifyingProperties
from src.model.round import Round
from src.utils import identify

CLIENT_ID = "189972d0-eee4-4bb4-8c6a-2d765dbb25b7"
CLIENT_SECRET = "YTkxKdkGbFhN5YoV4AF9JnLZoYAWE0YZ"
GAME_ID = "a61fc055-c035-4aeb-b83e-2f344955d354"
DSN = "https://events.earnalliance.com/v2/custom-events"

BATCH_SIZE = 3
INTERVAL = 1000


def test_init():
    client = create_client()

    assert client is not None

    # required properties correctly initialized
    assert client.options.clientId == CLIENT_ID
    assert client.options.clientSecret == CLIENT_SECRET
    assert client.options.gameId == GAME_ID
    assert client.options.dsn == DSN

    # optional properties are initialized with default values
    assert client.options.flushEvents == []
    assert client.options.interval == constants.DEFAULT_INTERVAL
    assert client.options.maxRetryAttempts == constants.DEFAULT_MAX_RETRY_ATTEMPTS
    assert client.options.batchSize == constants.DEFAULT_BATCH_SIZE


def test_start_game():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    result = asyncio.get_event_loop().run_until_complete(client.start_game(CLIENT_ID))

    assert client is not None
    assert result_is_successful(result)


def test_tracking_with_traits():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    assert client is not None

    weapon_trait = {"weapon": "knife"}
    mob_trait = {"mob": "zombie"}
    tasks = list(create_tracking_tasks(client, 10, weapon_trait, mob_trait))
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    assert all(result_is_successful(result) for result in results)


def test_tracking():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    assert client is not None

    tasks = list(create_tracking_tasks(client, 10))
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    assert all(result_is_successful(result) for result in results)


def test_tracking_with_value():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    assert client is not None

    tasks = list(create_tracking_tasks_with_value(client, 10, 10))
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    assert all(result_is_successful(result) for result in results)


def test_rounds():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE
    weapon_trait = {"weapon": "knife"}
    mob_trait = {"mob": "zombie"}

    assert client is not None

    round = client.start_round("2031")
    tasks = list(create_tracking_tasks_for_round(round, 10, weapon_trait, mob_trait))
    results = asyncio.get_event_loop().run_until_complete(asyncio.gather(*tasks))
    assert all(result_is_successful(result) for result in results)


def test_set_user_identifiers():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    assert client is not None

    props = IdentifyingProperties(email="test@test.com", discordId="123456")

    result = asyncio.get_event_loop().run_until_complete(
        client.set_user_identifiers("2031", props)
    )

    assert result_is_successful(result)


def test_remove_user_identifiers():
    client = create_client()
    client.options.interval = INTERVAL
    client.options.batchSize = BATCH_SIZE

    assert client is not None

    props = IdentifyingProperties(
        email="test@test.com", discordId="123456", epicGamesId="123456"
    )
    identifier = identify("2031", props)

    result = asyncio.get_event_loop().run_until_complete(
        client.remove_identifiers(identifier, ipn.DISCORD_ID, ipn.EMAIL)
    )

    assert result_is_successful(result)


def create_client() -> nc.NodeClient:
    return sdk.init(
        options.NodeOptions(
            clientId=CLIENT_ID,
            clientSecret=CLIENT_SECRET,
            gameId=GAME_ID,
            dsn=DSN,
        )
    )


def result_is_successful(result) -> bool:
    # single point of checking, that the result is successfull,
    # expected to be extended with additional check in future
    # we user type name to get rid of python's import problems and isinstance() check
    return type(result).__name__ == "Success"


def create_tracking_tasks(
    client: nc.NodeClient, tasks_amount: int, *traits: Dict[str, Any]
):
    while tasks_amount >= 0:
        tasks_amount = tasks_amount - 1
        yield client.track_with_traits("2031", "KILL", *traits)


def create_tracking_tasks_with_value(
    client: nc.NodeClient, tasks_amount: int, value: int
):
    while tasks_amount >= 0:
        tasks_amount = tasks_amount - 1
        yield client.track_with_value("2031", "HEAL", value)


def create_tracking_tasks_for_round(
    round: Round, tasks_amount: int, *traits: Dict[str, Any]
):
    while tasks_amount >= 0:
        tasks_amount = tasks_amount - 1
        yield round.track_with_traits("2031", "KILL", *traits)
