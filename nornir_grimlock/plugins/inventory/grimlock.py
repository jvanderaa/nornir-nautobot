"""Nornir Grimlock Inventory Plugin."""
# Python Imports
import sys
import logging
from os import getenv
from typing import Any, Dict, Union

# Nornir Imports
from nornir.core.inventory import (
    Inventory,
    Groups,
    Hosts,
    Defaults,
)

# Other third party imports
import pynetbox as pygrimlock
from requests import Session

# Create Logger
logger = logging.getLogger(__name__)

# Setup connection to Grimlock
class GrimlockInventory:
    """Grimlock Nornir Inventory."""

    def __init__(
        self,
        grimlock_url: Union[str, None],
        grimlock_token: Union[str, None],
        ssl_verify: Union[bool, None] = True,
        filter_parameters: Union[Dict[str, Any], None] = None,
    ) -> None:
        """Grimlock nornir class initialization."""
        self.grimlock_url = grimlock_url or getenv("GRIMLOCK_URL")
        self.grimlock_token = grimlock_token or getenv("GRIMLOCK_TOKEN")
        self.filter_parameters = filter_parameters
        self.ssl_verify = ssl_verify
        self._verify_required()
        self._api_session = None
        self._devices = None
        self._pygrimlock_obj = None

    def _verify_required(self) -> bool:
        """Verify that required parameters are provided either passed in or via environment.

        Returns:
            bool: Successful

        Raises:
            ValueError: When incorrect value is provided
        """
        for item in [self.grimlock_url, self.grimlock_token]:
            if item is None:
                raise ValueError("Missing URL or Token from parameters or environment.")

        return True

    @property
    def api_session(self):
        """Request session to pass into Grimlock."""
        if self._api_session is None:
            self._api_session = Session()
            self._api_session.headers.update({"Authorization": f"Token {self.grimlock_token}"})
            self._api_session.verify = self.ssl_verify

        return self._api_session

    @property
    def pygrimlock_obj(self) -> pygrimlock.core.api.Api:
        """Pygrimlock API object to interact with Grimlock.

        Returns:
            pyGrimlock object: Object to interact with the pygrimlock SDK.
        """
        if self._pygrimlock_obj is None:
            self._pygrimlock_obj = pygrimlock.api(self.grimlock_url, token=self.grimlock_token)
            self._pygrimlock_obj.http_session = self.api_session

        return self._pygrimlock_obj

    @property
    def devices(self) -> list:
        """Devices information from Grimlock."""
        if self._devices is None:
            # Check for filters. Cannot pass an empty dictionary to the filter method
            if self.filter_parameters is None:
                self._devices = self.pygrimlock_obj.dcim.devices.all()
            else:
                try:
                    self._devices = self.pygrimlock_obj.dcim.filter(**self.filter_parameters)
                except pygrimlock.core.query.RequestError:
                    print("Error in the query filters. Please verify the parameters.")
                    sys.exit(1)

        return self._devices

    # Build the inventory
    def load(self) -> Inventory:
        """Load of Nornir inventory.

        Returns:
            Inventory: Nornir Inventory
        """
        hosts = Hosts()
        groups = Groups()
        defaults = Defaults()

        for device in self.devices:
            # Set the base information for a device
            inv_dev: Dict[Any, Any] = {"data": {}}

            # Assign the pygrimlock host object to the data key
            inv_dev["data"]["pygrimlock_object"] = self.pygrimlock_obj.dcim.devices.get(name=device)

            # Add Primary IP address, if found. Otherwise add hostname as the device name
            inv_dev["hostname"] = None

            # Check for the device having a primary IP assigned
            if device.primary_ip:
                inv_dev["hostname"] = device.primary_ip.address.split("/")[0]
            else:
                # check to see if name of the device is not None, then assign this. Which will use DNS to connect to the device.
                if device.name is not None:
                    inv_dev["hostname"] = device["name"]

            # TODO: #1 DETERMINE COMMON GROUPING METHODS TO PROVIDE A WAY

            # Add host to hosts by name first, ID otherwise - to string
            hosts[device.name or str(device.id)] = inv_dev  # pylint: disable=unsupported-assignment-operation

        return Inventory(hosts=hosts, groups=groups, defaults=defaults)
