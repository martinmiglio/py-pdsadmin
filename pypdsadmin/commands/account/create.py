"""Command to create a new account in the PDS server."""

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


class AccountCreateCommand(Command):
    """Command to create a new account in the PDS server."""

    name = "account create"
    description = "Create a new account in the PDS server."

    arguments: list[Argument] = [  # noqa: RUF012
        argument("email", description="Email address for the new account."),
        argument("handle", description="Handle for the new account."),
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
        email = self.argument("email")
        handle = self.argument("handle")
        hostname = environ["PDS_HOSTNAME"]
        admin_password = environ["PDS_ADMIN_PASSWORD"]
        timeout = int(self.option("timeout"))

        if self.option("prompt-password"):
            password = self.secret("Enter a password for the new account")
        else:
            password = self.option("password")
            if not password:
                password = generate_secure_token(DEFAULT_PASSWORD_LENGTH)

        invite_response = requests.post(
            f"https://{hostname}/xrpc/com.atproto.server.createInviteCode",
            auth=("admin", admin_password),
            json={"useCount": 1},
            timeout=timeout,
        )
        invite_response.raise_for_status()
        invite_code = invite_response.json()["code"]

        account_response = requests.post(
            f"https://{hostname}/xrpc/com.atproto.server.createAccount",
            json={
                "email": email,
                "handle": handle,
                "password": password,
                "inviteCode": invite_code,
            },
            timeout=timeout,
        )

        try:
            account_response.raise_for_status()
        except requests.HTTPError:
            json = account_response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise

        did = account_response.json().get("did")

        self.line(f"Account created successfully!\nHandle: {handle}\nDID: {did}\nPassword: {password}")
