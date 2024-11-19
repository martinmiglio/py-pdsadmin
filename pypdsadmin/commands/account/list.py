"""Command to list accounts in the PDS server."""

from __future__ import annotations

from typing import TYPE_CHECKING

import requests
from cleo.commands.command import Command
from cleo.helpers import option

from pypdsadmin.consts import DEFAULT_TIMEOUT
from pypdsadmin.env import environ

if TYPE_CHECKING:
    from cleo.io.inputs.option import Option


class AccountListCommand(Command):
    """Command to list accounts in the PDS server."""

    name = "account list"
    description = "List accounts in the PDS server."

    options: list[Option] = [  # noqa: RUF012
        option("timeout", "t", description="The request timeout in seconds.", flag=False, default=DEFAULT_TIMEOUT),
        option("compact", "c", description="Compact the output.", flag=True),
    ]

    def handle(self) -> None:
        """Handle the command."""
        hostname = environ["PDS_HOSTNAME"]
        self.write("<comment>Fetching repos...</comment>")
        response = requests.get(
            f"https://{hostname}/xrpc/com.atproto.sync.listRepos?limit=100",
            timeout=int(self.option("timeout")),
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            json = response.json()
            self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
            raise
        repos = response.json().get("repos", [])

        output = []
        for repo in repos:
            self.overwrite(f"<comment>Fetching account info for {repo.get('did')}...</comment>")
            did = repo.get("did")
            account_response = requests.get(
                f"https://{hostname}/xrpc/com.atproto.admin.getAccountInfo?did={did}",
                auth=("admin", environ["PDS_ADMIN_PASSWORD"]),
                timeout=int(self.option("timeout")),
            )
            try:
                account_response.raise_for_status()
            except requests.HTTPError:
                json = account_response.json()
                self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
                raise
            output.append(account_response.json())

        if len(output) == 0:
            self.overwrite("<info>No accounts found.</info>")
            return
        self.overwrite("")
        self.render_table(
            ["Handle", "Email", "DID"],  # type: ignore  # noqa: PGH003
            [[row.get("handle", ""), row.get("email", ""), row.get("did", "")] for row in output],
            style="compact" if self.option("compact") else "default",
        )
