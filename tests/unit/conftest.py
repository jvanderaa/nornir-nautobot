"""Used to setup fixtures to be used through tests."""
import pytest


@pytest.fixture()
def give_me_success():
    """Provide True to make tests pass.

    Returns:
        (bool): Returns True
    """
    return True
