# Ghostty shell helpers; Vi editing remains scoped to its tmux server.
[[ -o interactive ]] || return
[[ ${TERM_PROGRAM:-} == ghostty || ( -n ${TMUX:-} && ${TMUX%%,*} == */ghostty-lab ) ]] || return
[[ -n ${_GHOSTTY_TMUX_VI_SETUP:-} ]] && return
typeset -g _GHOSTTY_TMUX_VI_SETUP=1

# Match the Ghostty prompt even when the user's zsh has no Starship setup.
export STARSHIP_CONFIG="$HOME/.config/ghostty/starship-zsh.toml"
if (( ! $+functions[prompt_starship_precmd] )); then
  eval "$("@BREW@/bin/starship" init zsh)"
fi

if [[ -n ${TMUX:-} && ${TMUX%%,*} == */ghostty-lab ]]; then
  bindkey -v
  function nu() {
    command "@BREW@/bin/nu" --config "@HOME@/.config/ghostty/nushell/config.nu" "$@"
  }
fi

function t() { "@HOME@/.config/ghostty/bin/tmux-shortcuts" start "$@"; }
function tn() { "@HOME@/.config/ghostty/bin/tmux-shortcuts" new "$@"; }
function tl() { "@HOME@/.config/ghostty/bin/tmux-shortcuts" list "$@"; }
function ta() { "@HOME@/.config/ghostty/bin/tmux-shortcuts" attach "$@"; }
function tk() { "@HOME@/.config/ghostty/bin/tmux-shortcuts" kill "$@"; }
alias ports='/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN'
alias kctx='kubectl config current-context'
alias kpods='kubectl get pods'
