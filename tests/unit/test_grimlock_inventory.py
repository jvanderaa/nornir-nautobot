"""Pytest of Grimlock Inventory."""
# Standard Library Imports
from os import path

# Third Party Imports
import pytest
from requests.sessions import Session
import pynetbox as pygrimlock
from requests_mock import Mocker

# Application Imports
from nornir_grimlock.plugins.inventory.grimlock import GrimlockInventory

# GLOBALS
HERE = path.abspath(path.dirname(__file__))
API_CALLS = [
    {
        "fixture_path": f"{HERE}/mocks/01_get_devices.json",
        "url": "http://mock.example.com/api/dcim/devices/",
        "method": "get",
    },
    {
        "fixture_path": f"{HERE}/mocks/02_get_device1.json",
        "url": "http://mock.example.com/api/dcim/devices/?name=den-dist01",
        "method": "get",
    },
    {
        "fixture_path": f"{HERE}/mocks/03_get_device2.json",
        "url": "http://mock.example.com/api/dcim/devices/?name=den-dist02",
        "method": "get",
    },
    {
        "fixture_path": f"{HERE}/mocks/04_get_device3.json",
        "url": "http://mock.example.com/api/dcim/devices/?name=den-wan01",
        "method": "get",
    },
]

# Functions for helping tests
def load_api_calls(mock):
    """Loads API calls for mocker

    Args:
        mock (Request Mock): Requests Mock instance
    """
    for api_call in API_CALLS:
        with open(api_call["fixture_path"], "r") as _file:
            api_call["text"] = _file.read()

        mock.request(method=api_call["method"], url=api_call["url"], text=api_call["text"], complete_qs=True)


#
# Tests
#
def test_grimlock_nornir_initialization():
    # Set a var
    no_exception_found = True
    try:
        GrimlockInventory(grimlock_url="http://localhost:8000", grimlock_token="0123456789abcdef01234567890")
    except:  # pylint: disable=bare-except
        no_exception_found = False

    assert no_exception_found


def test_grimlock_nornir_missing_url():
    with pytest.raises(ValueError) as err:
        GrimlockInventory(grimlock_url=None, grimlock_token="0123456789abcdef01234567890")

    assert str(err.value) == "Missing URL or Token from parameters or environment."


def test_grimlock_nornir_missing_token():
    with pytest.raises(ValueError) as err:
        GrimlockInventory(grimlock_url="http://localhost:8000", grimlock_token=None)

    assert str(err.value) == "Missing URL or Token from parameters or environment."


def test_api_session():
    test_class = GrimlockInventory(grimlock_url="http://localhost:8000", grimlock_token="0123456789abcdef01234567890")
    expected_headers = {
        "User-Agent": "python-requests/2.25.1",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Authorization": "Token 0123456789abcdef01234567890",
    }
    assert isinstance(test_class.api_session, Session)
    assert expected_headers == test_class.api_session.headers


def test_pygrimlock_obj():
    test_class = GrimlockInventory(grimlock_url="http://mock.example.com", grimlock_token="0123456789abcdef01234567890")
    assert isinstance(test_class.pygrimlock_obj, pygrimlock.api)


def test_devices():
    # Import mock requests
    with Mocker() as mock:
        load_api_calls(mock)
        test_class = GrimlockInventory(
            grimlock_url="http://mock.example.com", grimlock_token="0123456789abcdef01234567890"
        )
        pygrimlock_obj = pygrimlock.api(url="http://mock.example.com", token="0123456789abcdef01234567890")
        expected_devices = []
        for device in ["den-dist01", "den-dist02", "den-wan01"]:
            expected_devices.append(pygrimlock_obj.dcim.devices.get(name=device))

        assert test_class.devices == expected_devices
