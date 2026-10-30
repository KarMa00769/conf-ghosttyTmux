#!/usr/bin/env python3
"""macOS integration smoke test; uses a temporary HOME and isolated tmux socket."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

PROJECT = Path(__file__).resolve().parent.parent
if sys.platform != 'darwin':
    raise SystemExit('Esta prueba necesita macOS.')
programs = {n: shutil.which(n) for n in ['tmux', 'nu', 'starship', 'zoxide', 'fzf', 'carapace']}
missing = [k for k, v in programs.items() if not v]
if missing:
    raise SystemExit('Faltan dependencias en PATH: ' + ', '.join(missing))

with tempfile.TemporaryDirectory(prefix='ghostty-smoke-') as temp:
    root = Path(temp)
    home = root / 'home with spaces'
    home.mkdir()
    prefix = root / 'brew'
    (prefix / 'bin').mkdir(parents=True)
    for name, binary in programs.items():
        (prefix/'bin'/name).symlink_to(binary)
    brew = prefix/'bin/brew'
    brew.write_text('#!/bin/sh\n[ "$1" = --prefix ] && printf "%s\\n" "'+str(prefix)+'"\n')
    brew.chmod(0o755)
    dest = home/'.config/ghostty'
    dest.mkdir(parents=True)
    (dest/'config').write_text('original config\n')
    (home/'.zshrc').write_text('# original\n')
    global_nu = home/'Library/Application Support/nushell/config.nu'
    global_nu.parent.mkdir(parents=True)
    global_nu.write_text("$env.SMOKE_GLOBAL = 'loaded'\n")
    env = os.environ.copy()
    env.update(HOME=str(home), PATH=str(prefix/'bin')+':/usr/bin:/bin:/usr/sbin:/sbin', TERM='xterm-256color')
    env.pop('TMUX', None)
    env.pop('TMUX_PANE', None)
    def invoke(*args):
        result = subprocess.run(args, env=env, text=True, capture_output=True)
        if result.returncode:
            raise RuntimeError(f'{args}: {result.stderr}\n{result.stdout}')
        return result.stdout
    installer = str(PROJECT/'install.sh')
    invoke(installer, '--with-zsh', '--without-thumbs')
    invoke(installer, '--with-zsh', '--without-thumbs')
    with (home/'.zshrc').open('a') as f:
        f.write('# edit after installation\n')
    config = dest/'nushell/config.nu'
    assert invoke(programs['nu'], '--config', str(config), '--commands', 'print $env.SMOKE_GLOBAL').strip() == 'loaded'
    command = next(line.split('=', 1)[1].strip() for line in (dest/'config').read_text().splitlines() if line.startswith('command ='))
    assert command.startswith('shell:exec ')
    assert invoke('/bin/sh', '-c', command[len('shell:'):] + ' --commands \"print start-ok\"').strip() == 'start-ok'
    assert 'tmux-thumbs' not in (dest/'tmux.conf').read_text()
    ghostty = Path('/Applications/Ghostty.app/Contents/MacOS/ghostty')
    if ghostty.exists():
        invoke(str(ghostty), '+validate-config', '--config-file='+str(dest/'config'))
    socket = 'ghostty-smoke-'+str(os.getpid())
    for path in [config, dest/'start-tmux', dest/'bin/tmux-shortcuts', dest/'zsh/vi-mode.zsh']:
        path.write_text(path.read_text().replace('ghostty-lab', socket))
    try:
        invoke(programs['tmux'], '-L', socket, '-f', str(dest/'tmux.conf'), 'new-session', '-d', '-s', 'audit')
        time.sleep(.5)
        assert 'audit:' in invoke(programs['nu'], '--config', str(config), '--commands', 'tl')
        status = invoke(programs['tmux'], '-L', socket, 'list-panes', '-F', '#{pane_current_command}:#{pane_dead}')
        assert status.strip() == 'nu:0', status
        keys = invoke(programs['tmux'], '-L', socket, 'list-keys', '-T', 'prefix')
        assert '/scripts/scripts/floax.sh' not in keys
        assert '/scripts/floax.sh' in keys and '/scripts/menu.sh' in keys
    finally:
        subprocess.run([programs['tmux'], '-L', socket, 'kill-server'], env=env, capture_output=True)
    invoke(installer, '--uninstall')
    assert 'conf-ghosttyTmux' in (home/'.zshrc').read_text()
    invoke(installer, '--uninstall')
    assert (dest/'config').read_text() == 'original config\n'
    assert (home/'.zshrc').read_text() == '# original\n# edit after installation\n'
    print('OK: instalación, reinstalación, Nu, tmux y restauración con HOME temporal.')
