"""Used to setup fixtures to be used through tests."""
import os
import pytest
from nornir_nautobot.plugins.inventory.nautobot import NautobotInventory


@pytest.fixture()
def nautobot_nornir_class():
    """Provide True to make tests pass.

    Returns:
        (bool): Returns True
    """
    return NautobotInventory(nautobot_url="http://mock.example.com", nautobot_token="0123456789abcdef01234567890")


@pytest.fixture()
def delete_environment():
    """Deletes the environment loaded by pytest dotenv."""
    if os.getenv("NAUTOBOT_URL"):
        del os.environ["NAUTOBOT_URL"]
    if os.getenv("NAUTOBOT_TOKEN"):
        del os.environ["NAUTOBOT_TOKEN"]
