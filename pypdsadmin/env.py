"""Environment module."""

from __future__ import annotations

import logging
import os
import pathlib

import dotenv

from pypdsadmin.consts import DEFAULT_ENV_FILE, DEFAULT_PDS_ROOT


class Environment:
    """Environment class."""

    def __init__(self, env_file: pathlib.Path | str | os.PathLike[str] | None) -> None:
        """Initialize the Environment class."""
        if env_file is None:
            dotenv.load_dotenv()
            logging.debug("Environment file not specified. Using default.")
            return

        env_file = pathlib.Path(env_file)
        if env_file.exists():
            dotenv.load_dotenv(dotenv_path=env_file)
            logging.debug("Environment file found at %s.", env_file)
        else:
            logging.debug("Environment file not found at %s.", env_file)

    def __getitem__(self, var_name: str) -> str:
        """Get an environment variable.

        This function retrieves an environment variable. If the variable is not
        found, an error message is printed and the program exits.

        Args:
            var_name (str): The name of the environment variable to retrieve.

        Returns:
            str: The value of the environment variable.

        """
        value = os.getenv(var_name)
        if value is None:
            msg = f"Environment variable {var_name} not found."
            raise ValueError(msg)
        return value


root_env_file = pathlib.Path(DEFAULT_PDS_ROOT) / DEFAULT_ENV_FILE
if root_env_file.exists():
    environ = Environment(root_env_file)
else:
    local_env_file = pathlib.Path(DEFAULT_ENV_FILE)
    environ = Environment(local_env_file) if local_env_file.exists() else Environment(None)
