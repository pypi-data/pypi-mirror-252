import pytest

from src import options


def test_all_required_fields_present():
    opts = options.NodeOptions(
        clientId="test",
        clientSecret="test",
        dsn="test",
        gameId="test",
    )

    assert opts is not None


def test_one_required_field_absent():
    with pytest.raises(Exception) as ex:
        options.NodeOptions(
            clientId="test",
            clientSecret="test",
            gameId="test",
            dsn=None,
        )

    assert str(ex.value) == "required field value is missing: dsn"
