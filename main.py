import os
import platform
import sys
from pathlib import Path
from shutil import disk_usage, which, chown
from subprocess import run

from rich.console import Console
from rich.prompt import Confirm, Prompt

# noinspection SpellCheckingInspection
PACKAGES_TO_INSTALL = [
	"btop",
	"eza",
	"fd-find",
	"fzf",
	"qemu-guest-agent",
	"ripgrep",
	"stow",
	"tmux",
	"tmux-plugin-manager",
	"vnstat",
	"wget",
	"zoxide",
	"zsh",
	"zsh-autosuggestions",
	"zsh-syntax-highlighting",
]


def pre_check(console: Console, console_error: Console):
	if os.getuid() != 0:
		console.rule("Pre-Checks")
		console_error.print("Please run as root")
		sys.exit(1)

	# noinspection SpellCheckingInspection
	if platform.freedesktop_os_release()["ID"] not in ["ubuntu", "debian"]:
		console.rule("Pre-Checks")
		console.print("Only Ubuntu and Debian are supported. You may try to run the script at your own risk",
		              style="yellow")
		if not Confirm.ask("Continue?", default=False):
			sys.exit(1)


def install_packages(console: Console):
	run(["apt", "update"], check=True)

	upgrade_method_prompt = """Choose apt upgrade method:
1. apt upgrade (default, normally you should choose this)
2. apt full-upgrade (required on Proxmox VE / Proxmox Backup Server hosts, per the official Proxmox documentation)"""
	console.rule("Upgrade Method")
	console.print(upgrade_method_prompt)
	upgrade_method = Prompt.ask("Upgrade method", choices=['1', '2'], default='1')
	if upgrade_method == '1':
		run(["apt", "upgrade", "-y"], check=True)
	else:
		run(["apt", "full-upgrade", "-y"], check=True)

	# noinspection SpellCheckingInspection
	run(["apt", "autoremove", "-y"], check=True)
	run(["apt", "install", "-y", *PACKAGES_TO_INSTALL], check=True)


def add_ssh_key(console: Console):
	ssh_dir = Path.home() / ".ssh"
	ssh_dir.mkdir(mode=0o700, exist_ok=True)
	authorized_keys_file = ssh_dir / "authorized_keys"
	authorized_keys_file.touch(mode=0o600, exist_ok=True)

	with open(authorized_keys_file) as f:
		current_authorized_keys = f.read().strip()
	if current_authorized_keys != "":
		return

	console.rule("SSH Key Management")
	new_key = Prompt.ask("Enter new SSH public key to add (or leave empty to skip)", default="", show_default=False)
	if new_key:
		with open(authorized_keys_file, 'a') as f:
			f.write(new_key + "\n")


# noinspection SpellCheckingInspection
def change_timezone(console: Console):
	current_timezone = run(["timedatectl", "show", "-P", "Timezone"], capture_output=True, text=True).stdout.strip()

	if current_timezone != "Etc/UTC":
		return

	console.rule("Timezone Configuration")
	console.print(f"Current Timezone: {current_timezone}")
	new_timezone = Prompt.ask("Enter new timezone (e.g., 'Asia/Tokyo') or leave empty to skip", default="",
	                          show_default=False)

	if new_timezone:
		run(["timedatectl", "set-timezone", new_timezone], check=True)


def install_docker(console: Console):
	if which("docker") is not None:
		return

	console.rule("Docker Installation")
	if Confirm.ask("Install Docker?", default=False):
		run(["curl", "-fsSL", "https://get.docker.com", "-o", "get-docker.sh"], check=True)
		run(["sh", "get-docker.sh"], check=True)
		Path("get-docker.sh").unlink()


def enable_bbr():
	config_path = Path("/etc/sysctl.d/99-bbr.conf")

	if config_path.exists():
		return

	with open(config_path, 'w') as f:
		f.write("net.core.default_qdisc = cake\n")
		f.write("net.ipv4.tcp_congestion_control = bbr\n")
	run(["sysctl", "--system"], check=True)


# noinspection SpellCheckingInspection
def install_paping():
	if which("paping") is not None:
		return

	run(["wget",
	     "https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/paping/paping_1.5.5_x86-64_linux.tar.gz"],
	    check=True)
	run(["tar", "xf", "paping_1.5.5_x86-64_linux.tar.gz"], check=True)
	Path("paping_1.5.5_x86-64_linux.tar.gz").unlink()
	Path("paping").move_into("/usr/local/bin")
	chown("/usr/local/bin/paping", user="root", group="root")


def install_oh_my_zsh():
	if (Path.home() / ".oh-my-zsh").exists():
		return

	run(["wget", "https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh", "-O", "oh-my-zsh.sh"],
	    check=True)
	run(["sh", "oh-my-zsh.sh", "--unattended"], check=True)
	Path("oh-my-zsh.sh").unlink()
	# noinspection SpellCheckingInspection
	run(["chsh", "-s", "/usr/bin/zsh"], check=True)
	(Path.home() / ".zshrc").unlink()


def stow_dotfiles():
	dotfiles_dir = Path(__file__).parent / "dotfiles"

	for i in dotfiles_dir.iterdir():
		if i.is_dir():
			run(["stow", "--restow", i.name], cwd=dotfiles_dir, check=True)


def check_swap(console: Console):
	with open("/proc/meminfo") as f:
		for line in f:
			if line.startswith("MemTotal:"):
				mem_total_kb = int(line.split()[1])
			if line.startswith("SwapTotal:"):
				swap_total_kb = int(line.split()[1])
	disk_free_bytes = disk_usage("/").free

	mem_total_gb = mem_total_kb / 1024 / 1024
	swap_total_gb = swap_total_kb / 1024 / 1024
	disk_free_gb = round(disk_free_bytes / 1024 / 1024 / 1024)

	console.rule("Swap Check")

	console.print(f"Total Memory: {mem_total_gb:.2f} GB")
	console.print(f"Total Swap: {swap_total_gb:.2f} GB")
	console.print(f"Free Disk Space: {disk_free_gb} GB")

	console.input("Manually adjust swap size if necessary. Press Enter to continue...")


def main():
	console = Console()
	console_error = Console(stderr=True, style="red")

	pre_check(console, console_error)
	install_packages(console)
	add_ssh_key(console)
	change_timezone(console)
	install_docker(console)
	enable_bbr()
	install_paping()
	install_oh_my_zsh()
	stow_dotfiles()
	check_swap(console)

	console.print("Setup completed successfully. Consider rebooting the system.", style="green")


if __name__ == "__main__":
	main()
