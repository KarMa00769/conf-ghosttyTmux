# This config is used by Ghostty and its optional tmux sessions.
# @USER_NU_CONFIG@

$env.PATH = ($env.PATH | prepend ['@HOME@/.config/ghostty/bin' '@BREW@/bin' '@BREW@/sbin' '/usr/local/bin' '/usr/local/sbin'] | uniq)
$env.config.show_banner = false
$env.config.edit_mode = 'vi'
$env.config.cursor_shape.vi_insert = 'line'
$env.config.cursor_shape.vi_normal = 'block'
# Explicit tmux command: no session starts while loading this config.
def --wrapped tmux [...arguments: string] {
    if ($arguments | is-empty) {
        if (($env.TMUX? | default '') | is-not-empty) {
            print 'Ya estás dentro de tmux. Usa Ctrl+B y después d para desconectarte.'
        } else {
            ^"@HOME@/.config/ghostty/start-tmux"
        }
    } else {
        ^"@BREW@/bin/tmux" -L ghostty-lab -f "@HOME@/.config/ghostty/tmux.conf" ...$arguments
    }
}

# Completion and prompt integrations are local to Ghostty.
source "@HOME@/.config/ghostty/nushell/carapace.nu"
$env.STARSHIP_CONFIG = '@HOME@/.config/ghostty/starship.toml'
$env.STARSHIP_CACHE = '@HOME@/.config/ghostty/cache/starship'
use "@HOME@/.config/ghostty/nushell/starship-init.nu"

# Interactive finders and navigation, only in Ghostty.
$env._ZO_DATA_DIR = '@HOME@/.config/ghostty/data/zoxide'
source "@HOME@/.config/ghostty/nushell/zoxide-init.nu"

alias ll = ls --long
alias la = ls --all
alias gst = git status --short --branch
alias gd = git diff
alias gl = git log --oneline --graph --decorate -20
alias k = kubectl
alias kg = kubectl get
alias kd = kubectl describe
alias kl = kubectl logs
alias kctx = kubectl config current-context
alias kpods = kubectl get pods

# Short session commands use Ghostty's dedicated tmux server.
def t [] { ^"@HOME@/.config/ghostty/bin/tmux-shortcuts" start }
def tn [nombre: string] { ^"@HOME@/.config/ghostty/bin/tmux-shortcuts" new $nombre }
def tl [] { ^"@HOME@/.config/ghostty/bin/tmux-shortcuts" list }
def ta [nombre: string] { ^"@HOME@/.config/ghostty/bin/tmux-shortcuts" attach $nombre }
def tk [nombre: string] { ^"@HOME@/.config/ghostty/bin/tmux-shortcuts" kill $nombre }
def ports [] { ^/usr/sbin/lsof -nP -iTCP -sTCP:LISTEN }

# Prompt symbols for Nushell Vi editing modes.
$env.PROMPT_INDICATOR_VI_INSERT = {|| $"(ansi green_bold)❯ (ansi reset)" }
$env.PROMPT_INDICATOR_VI_NORMAL = {|| $"(ansi {fg: "#b4befe" attr: b})❮ (ansi reset)" }
