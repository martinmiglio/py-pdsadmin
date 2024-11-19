"""Command to untakedown an account in the PDS server."""

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


class AccountUntakedownCommand(Command):
    """Command to untakedown an account in the PDS server."""

    name = "account untakedown"
    description = "Untakedown an account in the PDS server."

    arguments: list[Argument] = [  # noqa: RUF012
        argument("did", description="DID of the account to untakedown."),
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
        timeout = self.option("timeout")

        if not did.startswith("did:"):
            msg = "DID parameter must start with 'did:'"
            raise ValueError(msg)

        pds_hostname = environ["PDS_HOSTNAME"]
        admin_password = environ["PDS_ADMIN_PASSWORD"]

        url = f"https://{pds_hostname}/xrpc/com.atproto.admin.updateSubjectStatus"
        payload = {
            "subject": {"$type": "com.atproto.admin.defs#repoRef", "did": did},
            "takedown": {"applied": False},
        }
        auth = ("admin", admin_password)

        response = requests.post(url, json=payload, auth=auth, timeout=timeout)

        try:
            response.raise_for_status()
        except requests.HTTPError:
            json = response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise

        self.line(f"<info>{did} untakedown successful.</info>")