# py-pdsadmin (Python PDS Admin)

A Python implementation of [pdsadmin](https://github.com/bluesky-social/pds/tree/main/pdsadmin), installable with pipx.

## Installation

```bash
pipx install py-pdsadmin
```

## Usage

```bash
pdsadmin list
```

```plaintext
Available commands:
  create-invite-code      Create an invite code for the PDS server.
  help                    Displays help for a command.
  list                    Lists commands.
  request-crawl           Request a crawl of a PDS instance.

 account
  account create          Create a new account in the PDS server.
  account delete          Delete an account from the PDS server.
  account list            List accounts in the PDS server.
  account reset-password  Reset the password of an account in the PDS server.
  account takedown        Take down an account from the PDS server.
  account untakedown      Untakedown an account in the PDS server.
  account update-handle   Update the handle of an account in the PDS server.
  ```

### Notes on Usage

Environment variables are automatically loaded from `/pds/pds.env` if it exists. This file is created by the [pds](https://github.com/bluesky-social/pds/tree/main) installation script. If you are not using the default installation, the script will look for `pds.env` or `.env` in the current working directory.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
