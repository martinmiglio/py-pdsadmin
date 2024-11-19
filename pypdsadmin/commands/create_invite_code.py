"""Command to create an invite code for the PDS server."""

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


class CreateInviteCodeCommand(Command):
    """Command to create an invite code for the PDS server."""

    name = "create-invite-code"
    description = "Create an invite code for the PDS server."

    arguments: list[Argument] = [  # noqa: RUF012
        argument(
            "use count",
            description="The number of times the invite code can be used.",
            optional=True,
            default="1",
        ),
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
        try:
            use_count = int(self.argument("use count"))
        except ValueError as e:
            msg = "Use count must be an integer"
            raise ValueError(msg) from e

        hostname = environ["PDS_HOSTNAME"]
        admin_password = environ["PDS_ADMIN_PASSWORD"]

        # create the invite code
        self.line(
            f"<comment>Creating invite code for <info>{hostname}</info>"
            f" with <info>{use_count}</info> uses...</comment>",
        )
        self.write("<comment>Making request...</comment>")
        response = requests.post(
            f"https://{hostname}/xrpc/com.atproto.server.createInviteCode",
            auth=("admin", admin_password),
            headers={"Content-Type": "application/json"},
            json={"useCount": use_count},
            timeout=int(self.option("timeout")),
        )

        try:
            response.raise_for_status()
        except requests.HTTPError:
            json = response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise

        invite_code = response.json()["code"]

        # print the invite code
        self.overwrite(
            f"<info>Invite code created successfully: <fg=black;bg=cyan;options=bold>{invite_code}</></info>\n",
        )
