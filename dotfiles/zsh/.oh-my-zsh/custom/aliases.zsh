# tmux
alias ,t="tmux a || tmux"

# fd: search hidden files and directories
alias fd="fdfind --hidden"

# eza
alias l="eza -l --no-permissions --no-user --no-time --no-filesize"
alias ll="eza -l --no-permissions --no-user --no-time --no-filesize -a"

# bat
alias bat="batcat"
alias cat="bat"

# update
alias ,u="cd /root/server-bootstrap && git pull && ./update.sh"
alias ,up=",u && poweroff"
alias ,ur=",u && reboot"
