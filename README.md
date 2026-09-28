# server-bootstrap

An interactive script that sets up a freshly installed server and can be rerun later to keep it up to date.

## What it does

Some examples of the changes it makes:

- Installs useful tools, such as fd, ripgrep, and zoxide
- Optionally adds an SSH key, changes the timezone, and installs Docker
- Installs Oh My Zsh
- Customizes zsh, tmux, vim, and a few other tools

See `bootstrap.sh` and `main.py` for all the steps.
See the `dotfiles` directory for the configuration files.

Note that this project reflects personal preferences (obviously).
Consider forking it and adjusting it to fit your own.

## Target environment

- OS
	- latest Ubuntu LTS
	- latest Proxmox VE (based on the latest Debian stable)
	- latest Proxmox Backup Server (based on the latest Debian stable)
- amd64
- running as the root account

This project was developed with only these environments in mind and has only been tested on them.
It may work elsewhere, but use it at your own risk.

## Usage

```shell
cd /root
git clone https://github.com/Resend1298/server-bootstrap.git
cd server-bootstrap
./bootstrap.sh
```

Keep the cloned repository where it is afterward: the dotfiles are symlinked into it.

## Updating

```shell
git pull
uv run main.py
```

## Running on an existing server

Existing files will not be overwritten, and the script will stop if it finds any.
Move or delete them, then rerun the script.

## License

[MIT](LICENSE)
