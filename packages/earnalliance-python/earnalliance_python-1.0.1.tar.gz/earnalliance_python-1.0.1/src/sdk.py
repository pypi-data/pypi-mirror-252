import os

from options import NodeOptions
from .client import NodeClient
import constants


def set_from_env(property_value, property_consumer, property_name):
    """Sets the property from the environment variable if it is not already set."""
    if property_value is None:
        env = os.environ.get(property_name)
        if env is not None:
            property_consumer(env)


def set_from_default(property_value, property_consumer, default_value):
    """Sets the property from the default value if it is not already set."""
    if property_value is None:
        property_consumer(default_value)


def init(options: NodeOptions) -> NodeClient:
    """Initializes the NodeClient"""

    set_from_env(
        options.clientId,
        lambda value: setattr(options, "clientId", value),
        constants.ENV_ALLIANCE_CLIENT_ID,
    )

    set_from_env(
        options.clientSecret,
        lambda value: setattr(options, "clientSecret", value),
        constants.ENV_ALLIANCE_CLIENT_SECRET,
    )

    set_from_env(
        options.dsn,
        lambda value: setattr(options, "dsn", value),
        constants.ENV_ALLIANCE_DSN,
    )

    set_from_env(
        options.gameId,
        lambda value: setattr(options, "gameId", value),
        constants.ENV_ALLIANCE_GAME_ID,
    )

    set_from_default(
        options.batchSize,
        lambda value: setattr(options, "batchSize", value),
        constants.DEFAULT_BATCH_SIZE,
    )

    set_from_default(
        options.interval,
        lambda value: setattr(options, "interval", value),
        constants.DEFAULT_INTERVAL,
    )

    set_from_default(
        options.maxRetryAttempts,
        lambda value: setattr(options, "maxRetryAttempts", value),
        constants.DEFAULT_MAX_RETRY_ATTEMPTS,
    )

    return NodeClient(options)
