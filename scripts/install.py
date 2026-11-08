#!/usr/bin/env python3
"""Install the macOS Ghostty setup without overwriting existing files."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parent.parent
TEMPLATE = PROJECT / 'templates' / 'ghostty'
HOME = Path.home()
DEST = HOME / '.config' / 'ghostty'
STATE = HOME / '.local' / 'state' / 'conf-ghosttyTmux'
MARK_START = '# >>> conf-ghosttyTmux >>>'
MARK_END = '# <<< conf-ghosttyTmux <<<'
FILES = ['config', 'tmux.conf', 'starship.toml', 'starship-zsh.toml', 'start-tmux', 'bin/tmux-shortcuts',
         'nushell/config.nu', 'nushell/carapace.nu', 'nushell/starship-init.nu',
         'nushell/zoxide-init.nu', 'zsh/vi-mode.zsh']
PLUGINS = ['tmux-sessionx', 'tmux-floax', 'tmux-resurrect', 'tmux-thumbs']


def fail(message):
    raise SystemExit(message)


def exists(path):
    return path.exists() or path.is_symlink()


def backup_dir(label):
    STATE.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=label+'-'+dt.datetime.now().strftime('%Y%m%d-%H%M%S')+'-', dir=STATE))


def uninstall():
    manifest_path = STATE / 'latest.json'
    if not manifest_path.exists():
        fail('No se encontró una instalación registrada para desinstalar.')
    manifest = json.loads(manifest_path.read_text())
    backup = Path(manifest['backup'])
    if not backup.is_dir():
        fail('Falta el respaldo de la instalación: '+str(backup))
    for record in manifest['files']:
        original = backup / 'files' / record['path']
        if record['had_original'] and not exists(original):
            fail('Falta el archivo original respaldado: '+str(original))
    undo = backup_dir('desinstalacion')
    for record in reversed(manifest['files']):
        relative = Path(record['path'])
        dest, original = DEST / relative, backup / 'files' / relative
        if record['had_original'] and not exists(original):
            fail('Falta el archivo original respaldado: '+str(original))
        if exists(dest):
            saved = undo / 'files' / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(saved))
        if record['had_original']:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(original), str(dest))
    if manifest.get('zsh_added'):
        zshrc = HOME / '.zshrc'
        if zshrc.exists():
            content = zshrc.read_text()
            block = manifest['zsh_block']
            if block in content:
                zshrc.write_text(content.replace(block, '', 1))
            else:
                print('El bloque de .zshrc cambió; revísalo manualmente.')
    prior = manifest.get('previous_manifest')
    if prior:
        manifest_path.write_text(json.dumps(prior, indent=2)+'\n')
    else:
        manifest_path.unlink()
    print('Desinstalación completada. Archivos retirados respaldados en:', undo)


def main():
    parser = argparse.ArgumentParser(description='Instalador de Ghostty + tmux para macOS')
    parser.add_argument('--install-deps', action='store_true', help='Instala dependencias con Homebrew')
    parser.add_argument('--with-zsh', action='store_true', help='Opción conservada por compatibilidad; zsh se configura por defecto')
    parser.add_argument('--without-thumbs', action='store_true', help='Omite tmux-thumbs y Rust')
    parser.add_argument('--uninstall', action='store_true', help='Deshace la última instalación y restaura sus respaldos')
    args = parser.parse_args()
    if sys.platform != 'darwin':
        fail('Esta versión está preparada solo para macOS. El soporte Linux vendrá después.')
    if args.uninstall:
        return uninstall()
    home = str(HOME)
    if any(ch in home for ch in "'\"\\\n\r$`"):
        fail('La ruta HOME contiene caracteres especiales no compatibles; revisa los requisitos del README.')
    brew = shutil.which('brew')
    if not brew:
        fail('Se requiere Homebrew: https://brew.sh/ (después ejecuta de nuevo ./install.sh).')
    prefix = subprocess.check_output([brew, '--prefix'], text=True).strip()
    if any(ch in prefix for ch in "'\"\\\n\r :"):
        fail('El prefijo de Homebrew contiene caracteres no compatibles: '+prefix)
    formulas = ['tmux','nushell','starship','zoxide','fzf','carapace']
    if not args.without_thumbs:
        formulas.append('rust')
    if args.install_deps:
        subprocess.run([brew, 'install', *formulas], check=True)
        casks = ['font-jetbrains-mono-nerd-font']
        if not Path('/Applications/Ghostty.app').exists():
            casks.insert(0, 'ghostty')
        subprocess.run([brew, 'install', '--cask', *casks], check=True)
    required = ['tmux','nu','starship','zoxide','fzf','carapace']
    missing = [name for name in required if not os.access(Path(prefix)/'bin'/name, os.X_OK)]
    if missing:
        fail('Faltan dependencias en '+prefix+'/bin: '+', '.join(missing)+'\nEjecuta ./install.sh --install-deps o instálalas con Homebrew.')
    cargo = shutil.which('cargo') or (str(Path(prefix)/'bin/cargo') if os.access(Path(prefix)/'bin/cargo', os.X_OK) else None)
    if not args.without_thumbs and not cargo:
        fail('tmux-thumbs necesita Rust/cargo. Instala rust o usa --without-thumbs.')
    if not Path('/Applications/Ghostty.app').exists() and not args.install_deps:
        print('Aviso: no se encontró /Applications/Ghostty.app. Puedes instalar Ghostty después.')
    plugins = [p for p in PLUGINS if not (args.without_thumbs and p == 'tmux-thumbs')]
    targets = FILES + ['plugins/'+p for p in plugins]
    global_nu = HOME / 'Library/Application Support/nushell/config.nu'
    source_nu = 'source "'+str(global_nu)+'"' if global_nu.is_file() else '# Sin configuración global de Nushell.'
    with tempfile.TemporaryDirectory(prefix='ghostty-setup-') as temp:
        stage = Path(temp) / 'ghostty'
        shutil.copytree(TEMPLATE, stage)
        for path in stage.rglob('*'):
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except (UnicodeError, OSError):
                continue
            if '@HOME@' not in text and '@BREW@' not in text and '@USER_NU_CONFIG@' not in text:
                continue
            text = text.replace('# @USER_NU_CONFIG@', source_nu).replace('@HOME@',home).replace('@BREW@',prefix)
            if args.without_thumbs and path == stage/'tmux.conf':
                text = '\n'.join(line for line in text.splitlines() if 'tmux-thumbs' not in line and '@thumbs-' not in line and 'C-S-F6' not in line)+'\n'
            path.write_text(text)
        if not args.without_thumbs:
            print('Compilando tmux-thumbs para la arquitectura de esta Mac…', flush=True)
            subprocess.run([cargo,'build','--locked','--release'], cwd=stage/'plugins/tmux-thumbs', check=True)
        backup = backup_dir('instalacion')
        manifest_path = STATE/'latest.json'
        previous_manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else None
        manifest = {'backup':str(backup), 'files':[], 'previous_manifest':previous_manifest, 'zsh_added':False}
        try:
            for rel in targets:
                dest, source = DEST/rel, stage/rel
                record = {'path':rel, 'had_original':exists(dest)}
                if record['had_original']:
                    saved = backup/'files'/rel
                    saved.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dest),str(saved))
                manifest['files'].append(record)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if source.is_dir(): shutil.copytree(source,dest,symlinks=True)
                else: shutil.copy2(source,dest)
            zshrc = HOME/'.zshrc'
            content = zshrc.read_text() if zshrc.exists() else ''
            if MARK_START not in content:
                if zshrc.exists():
                    shutil.copy2(zshrc, backup/'zshrc.original')
                block = '\n'+MARK_START+'\n[[ -r "$HOME/.config/ghostty/zsh/vi-mode.zsh" ]] && source "$HOME/.config/ghostty/zsh/vi-mode.zsh"\n'+MARK_END+'\n'
                zshrc.write_text(content+block)
                manifest['zsh_added']=True
                manifest['zsh_block']=block
            manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
        except BaseException:
            if manifest.get('zsh_added'):
                zshrc = HOME/'.zshrc'
                if zshrc.exists():
                    zshrc.write_text(zshrc.read_text().replace(manifest['zsh_block'], '', 1))
            for record in reversed(manifest['files']):
                dest=DEST/record['path']; original=backup/'files'/record['path']
                if exists(dest):
                    if dest.is_dir() and not dest.is_symlink(): shutil.rmtree(dest)
                    else: dest.unlink()
                if record['had_original'] and exists(original):
                    dest.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(original),str(dest))
            raise
    print('Instalación completa. Respaldo:', backup)
    print('Abre Ghostty y ejecuta t o tmux para entrar a tmux.')
    print('Recarga Ghostty con Cmd+Shift+, o reinícialo.')

if __name__ == '__main__':
    main()
