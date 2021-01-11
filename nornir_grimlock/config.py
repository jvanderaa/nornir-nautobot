"""Config module to load settings."""
# pylint: disable=no-name-in-module
import sys
from pathlib import Path
from typing import List, Optional

import toml
from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl, IPvAnyAddress, IPvAnyNetwork
from pydantic.types import DirectoryPath, FilePath, SecretStr
from pydantic.error_wrappers import ValidationError

SETTINGS = None
ENV_FILE_PATH = Path(__file__) / ".." / ".." / ".env"


class Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    """Main Settings Class for the project.

    The type of each setting is defined using Python annotations and Pydantic field types
    and is validated when a config file is loaded with Pydantic.
    """

    string_required: str
    secret_optional: Optional[SecretStr]  # pylint: disable=unsubscriptable-object
    array_default: List[str] = list()
    url_default: AnyHttpUrl = "http://localhost"
    ip_address: IPvAnyAddress = "192.168.0.1"
    ip_network: IPvAnyNetwork = "2001:db8:3c4d:15::/64"
    file: FilePath = "some/path/file.txt"
    directory: DirectoryPath = "some/path/"

    class Config:  # pylint: disable=too-few-public-methods
        """Config class to be used for Settings."""

        env_prefix = "NORNIR_GRIMLOCK_"
        env_file = ENV_FILE_PATH.resolve()
        env_file_encoding = "utf-8"


def load(config_file_name="nornir-grimlock.toml"):
    """Load a configuration file in nornir-grimlock.toml format that contains the settings.

    If nothing is found in the config file or if the config file do not exist, the default values will be used.

    Args:
        config_file_name (str, optional): Name of the configuration file to load. Defaults to "nornir-grimlock.toml".
    """
    global SETTINGS  # pylint: disable=global-statement
    config_file = Path(config_file_name)

    if config_file.exists():
        config_tmp = toml.loads(config_file.read_text())

        try:
            SETTINGS = Settings(**config_tmp)
            return
        except ValidationError as err:
            print(f"Configuration not valid, found {len(err.errors())} error(s)")
            for error in err.errors():
                print(f"  {'/'.join(error['loc'])} | {error['msg']} ({error['type']})")
            sys.exit(1)

    SETTINGS = Settings()
