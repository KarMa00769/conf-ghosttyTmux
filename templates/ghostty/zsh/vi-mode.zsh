# Ghostty shell helpers, scoped to Ghostty and its dedicated tmux server.
[[ -o interactive ]] || return
[[ ${TERM_PROGRAM:-} == ghostty || ( -n ${TMUX:-} && ${TMUX%%,*} == */ghostty-lab ) ]] || return
[[ -n ${_GHOSTTY_TMUX_VI_SETUP:-} ]] && return
typeset -g _GHOSTTY_TMUX_VI_SETUP=1
export PATH="$HOME/.config/ghostty/bin:@BREW@/bin:@BREW@/sbin:$PATH"
export STARSHIP_CONFIG="$HOME/.config/ghostty/starship-zsh.toml"
if (( ! $+functions[prompt_starship_precmd] )); then
  eval "$("@BREW@/bin/starship" init zsh)"
fi
export _ZO_DATA_DIR="$HOME/.config/ghostty/data/zoxide"
if (( ! $+functions[__zoxide_z] )); then
  eval "$("@BREW@/bin/zoxide" init zsh)"
fi
if [[ -n ${TMUX:-} && ${TMUX%%,*} == */ghostty-lab ]]; then
  bindkey -v
fi
function nu() { command "@BREW@/bin/nu" --config "$HOME/.config/ghostty/nushell/config.nu" "$@"; }
function tmux() {
  if (( $# == 0 )); then
    "$HOME/.config/ghostty/bin/tmux-shortcuts" start
  else
    command "@BREW@/bin/tmux" -L ghostty-lab -f "$HOME/.config/ghostty/tmux.conf" "$@"
  fi
}
function t() { "$HOME/.config/ghostty/bin/tmux-shortcuts" start "$@"; }
function tn() { "$HOME/.config/ghostty/bin/tmux-shortcuts" new "$@"; }
function tl() { "$HOME/.config/ghostty/bin/tmux-shortcuts" list "$@"; }
function ta() { "$HOME/.config/ghostty/bin/tmux-shortcuts" attach "$@"; }
function tk() { "$HOME/.config/ghostty/bin/tmux-shortcuts" kill "$@"; }
alias ports='/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN'
alias kctx='kubectl config current-context'
alias kpods='kubectl get pods'
alias gst='git status --short --branch'
alias gd='git diff'
alias gl='git log --oneline --graph --decorate -20'
alias k='kubectl'
alias kg='kubectl get'
alias kd='kubectl describe'
alias kl='kubectl logs'
