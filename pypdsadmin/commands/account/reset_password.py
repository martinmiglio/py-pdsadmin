"""Command to reset the password of an account in the PDS server."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from cleo.commands.command import Command
from cleo.helpers import argument, option

from pypdsadmin.consts import DEFAULT_PASSWORD_LENGTH, DEFAULT_TIMEOUT
from pypdsadmin.env import environ
from pypdsadmin.lib.tokens import generate_secure_token

if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument
    from cleo.io.inputs.option import Option


class AccountResetPasswordCommand(Command):
    """Command to reset the password of an account in the PDS server."""

    name = "account reset-password"
    description = "Reset the password of an account in the PDS server."

    arguments: list[Argument] = [  # noqa: RUF012
        argument("did", description="DID of the account to reset the password for."),
    ]

    options: list[Option] = [  # noqa: RUF012
        option(
            "timeout",
            "t",
            description="The request timeout in seconds.",
            flag=False,
            default=DEFAULT_TIMEOUT,
        ),
        option(
            "prompt-password",
            "-P",
            description="Prompt for a password instead of using a generated one.",
            flag=True,
        ),
        option(
            "password",
            "-p",
            description="Password for the new account.",
            flag=False,
            default=None,
        ),
    ]

    def handle(self) -> None:
        """Handle the command."""
        did = self.argument("did")
        timeout = self.option("timeout")

        if not did.startswith("did:"):
            msg = "DID parameter must start with 'did:'"
            raise ValueError(msg)

        pds_hostname = environ["PDS_HOSTNAME"]
        admin_password = environ["PDS_ADMIN_PASSWORD"]
        if self.option("prompt-password"):
            password = self.secret("Enter a password for the new account")
        else:
            password = self.option("password")
            if not password:
                password = generate_secure_token(DEFAULT_PASSWORD_LENGTH)

        url = f"https://{pds_hostname}/xrpc/com.atproto.admin.updateAccountPassword"
        payload = {"did": did, "password": password}
        auth = ("admin", admin_password)

        response = requests.post(url, json=payload, auth=auth, timeout=timeout)

        try:
            response.raise_for_status()
        except requests.HTTPError:
            json = response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise

        self.line("<info>Password reset successfully!</info>")
        self.line(f"<info>DID: {did}</info>")
        self.line(f"<info>New password: {password}</info>")
