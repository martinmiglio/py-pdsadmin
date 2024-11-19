"""Command to delete an account from the PDS server."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from cleo.commands.command import Command
from cleo.helpers import argument, option

from pypdsadmin.consts import DEFAULT_TIMEOUT
from pypdsadmin.env import environ

if TYPE_CHECKING:
    from cleo.io.inputs.argument import Argument
    from cleo.io.inputs.option import Option


class AccountDeleteCommand(Command):
    """Command to delete an account from the PDS server."""

    name = "account delete"
    description = "Delete an account from the PDS server."

    arguments: list[Argument] = [  # noqa: RUF012
        argument("did", description="DID of the account to delete."),
    ]

    options: list[Option] = [  # noqa: RUF012
        option(
            "timeout",
            "t",
            description="The request timeout in seconds.",
            flag=False,
            default=DEFAULT_TIMEOUT,
        ),
    ]

    def handle(self) -> None:
        """Handle the command."""
        did = self.argument("did")
        if not did.startswith("did:"):
            self.line_error("<error>DID must start with 'did:'</error>")
            return

        hostname = environ["PDS_HOSTNAME"]
        admin_password = environ["PDS_ADMIN_PASSWORD"]
        timeout = int(self.option("timeout"))

        confirmation = self.confirm(f"This action is permanent. Delete account {did}?", default=False)
        if not confirmation:
            self.line("<comment>Operation cancelled.</comment>")
            return

        response = requests.post(
            f"https://{hostname}/xrpc/com.atproto.admin.deleteAccount",
            auth=("admin", admin_password),
            json={"did": did},
            timeout=timeout,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:
            json = response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise

        self.line(f"<info>{did} deleted successfully.</info>")
