"""Main module for the CLI application."""

from cleo.application import Application

from pypdsadmin.commands import CreateInviteCodeCommand, RequestCrawlCommand
from pypdsadmin.commands.account import (
    AccountCreateCommand,
    AccountDeleteCommand,
    AccountListCommand,
    AccountResetPasswordCommand,
    AccountTakedownCommand,
    AccountUntakedownCommand,
    AccountUpdateHandleCommand,
)

application = Application()
application.add(CreateInviteCodeCommand())
application.add(RequestCrawlCommand())
application.add(AccountListCommand())
application.add(AccountCreateCommand())
application.add(AccountDeleteCommand())
application.add(AccountResetPasswordCommand())
application.add(AccountTakedownCommand())
application.add(AccountUntakedownCommand())
application.add(AccountUpdateHandleCommand())


def main() -> None:
    """Run the CLI application."""
    application.run()


if __name__ == "__main__":
    main()
