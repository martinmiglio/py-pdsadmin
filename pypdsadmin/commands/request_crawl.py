"""Request a crawl of a PDS instance."""

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


class RequestCrawlCommand(Command):
    """Command to request a crawl of a PDS instance."""

    name = "request-crawl"
    description = "Request a crawl of a PDS instance."

    arguments: list[Argument] = [  # noqa: RUF012
        # relay_hosts is a list of hosts to request a crawl from
        argument(
            "relay_hosts",
            description="The relay hosts to request a crawl from. Multiple hosts can be separated by commas."
            " If not provided, the PDS_CRAWLERS environment variable will be used.",
            optional=True,
            default="",
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
        relay_hosts = self.argument("relay_hosts")
        if not relay_hosts:
            relay_hosts = environ["PDS_CRAWLERS"]

        if not relay_hosts:
            msg = "Missing RELAY HOST parameter"
            raise ValueError(msg)

        for host in relay_hosts.split(","):
            self.line(f"<comment>Requesting crawl from <info>{host}</info></comment>")
            if not host.startswith(("https:", "http:")):
                host = f"https://{host}"  # noqa: PLW2901
            response = requests.post(
                f"{host}/xrpc/com.atproto.sync.requestCrawl",
                headers={"Content-Type": "application/json"},
                json={"hostname": environ["PDS_HOSTNAME"]},
                timeout=int(self.option("timeout")),
            )
            try:
                response.raise_for_status()
            except requests.HTTPError:
                json = response.json()
                self.line(f"<error>Error: {json.get('error')} - {json.get('message')}</error>")
                continue

        self.line("<comment>Done!</comment>")
