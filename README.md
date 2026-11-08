# Ghostty + tmux · Tokyo Night

Una configuración personal para macOS: Ghostty, tmux y zsh con colores Tokyo Night Storm, paneles con WASD y comandos cortos para sesiones. Ghostty abre zsh; tmux se inicia manualmente. Nushell sigue disponible con `nu`.

> Estado: primera versión para macOS. Probada en Apple Silicon con Ghostty 1.4, tmux 3.7 y Nushell 0.115. Intel usa el prefijo de Homebrew detectado, pero aún no se ha probado en una Mac Intel. Linux queda para una versión posterior.

## Instalación

Necesitas [Homebrew](https://brew.sh/) y Python 3. En macOS, Python también se puede instalar con `brew install python`.

```sh
git clone https://github.com/KarMa00769/conf-ghosttyTmux.git
cd conf-ghosttyTmux
./install.sh --install-deps
```

`--install-deps` pide a Homebrew instalar Ghostty, JetBrainsMono Nerd Font, tmux, Nushell, Starship, Zoxide, fzf, Carapace y Rust. Rust compila tmux-thumbs para la arquitectura de la Mac. Los plugins de tmux se incluyen como código fuente en este repo.

Si ya tienes las dependencias, ejecuta `./install.sh`. Para omitir tmux-thumbs y no necesitar Rust, usa `./install.sh --without-thumbs`; sus atajos no estarán disponibles. El instalador añade un bloque identificable a `~/.zshrc` para habilitar las integraciones en zsh de Ghostty. Las demás shells de zsh no se modifican.

El instalador escribe archivos gestionados en `~/.config/ghostty` y guarda cualquier versión anterior en `~/.local/state/conf-ghosttyTmux/`. Si existe el archivo global de configuración de Nushell en la ubicación estándar de macOS, la configuración de Ghostty lo carga primero. Los datos de sesiones, historiales y archivos de usuario permanecen en la máquina. Se admiten espacios en `HOME`; por seguridad, el instalador rechaza comillas, `$`, acentos graves, barras invertidas y saltos de línea en esa ruta.

Abre Ghostty y ejecuta `t` o `tmux` para entrar a tmux. Para cargar cambios de configuración de Ghostty, pulsa `Cmd+Shift+,` o reinicia la app. Cada shell nueva carga la configuración actualizada.

## Comandos

Disponibles en zsh y Nushell de Ghostty:

| Comando | Acción |
| --- | --- |
| `t` | Abre tmux o retoma una sesión desconectada. |
| `tn uni` | Crea la sesión `uni` y entra en ella. |
| `tl` | Lista las sesiones. |
| `ta uni` | Entra en `uni`. |
| `tk uni` | Elimina exactamente `uni` y termina los procesos de esa sesión. |
| `ports` | Lista puertos TCP que están escuchando en macOS. |
| `kctx` | Muestra el contexto actual de Kubernetes. |
| `kpods` | Lista pods; acepta opciones, por ejemplo `kpods -A`. |

`kctx` y `kpods` requieren `kubectl` y una configuración de Kubernetes; el instalador no los instala ni cambia contextos. Ambas shells incluyen `gst`, `gd`, `gl`, `k`, `kg`, `kd`, `kl`, `z` y `zi`; `ll` y `la` dependen de la configuración de cada shell.

## Atajos dentro de tmux

| Teclas | Acción |
| --- | --- |
| `Cmd+T` | Nueva ventana. |
| `Cmd+D` / `Cmd+Shift+D` | Dividir panel a la derecha / abajo. |
| `Cmd+W` | Cerrar el panel activo. |
| `Cmd+Enter` | Ampliar o restaurar el panel. |
| `Cmd+R`, WASD, `Esc` | Mover el foco entre paneles. |
| `Cmd+Shift+R`, WASD, `Esc` | Cambiar tamaño del panel; `A` amplía el ancho y `D` lo reduce. |
| `Cmd+1` … `Cmd+9` | Elegir ventana. |
| `Cmd+Shift+P` | Selector de sesiones. |
| `Cmd+Shift+N` | Crear sesión con nombre. |
| `Cmd+F` | Buscar en el historial del panel. |
| `Cmd+Shift+F` o `Cmd+Shift+B` | Terminal flotante. |
| `Cmd+Shift+Y` | Copiar texto visible con tmux-thumbs. |

El prefijo de tmux es `Ctrl+B`: después, `s` abre el selector de sesiones, `f` la terminal flotante, `Espacio` activa Thumbs, `Ctrl+S` guarda una sesión y `Ctrl+R` la restaura. Resurrect está configurado para guardar manualmente la distribución, sin reiniciar programas automáticamente.

## Actualizar o desinstalar

Actualiza el repositorio con Git y vuelve a ejecutar el instalador con las mismas opciones. Cada instalación crea otro respaldo. Para deshacer la **última** instalación:

```sh
./install.sh --uninstall
```

Se restauran los archivos anteriores de esa instalación y los archivos retirados se guardan en otro respaldo. Si se añadió el bloque de zsh, se quita sin reemplazar el resto de `.zshrc`. Una desinstalación repetida retrocede una instalación más. No desinstala paquetes de Homebrew ni borra historial o sesiones.

## Validación

Con las dependencias instaladas y disponibles en `PATH`, `python3 tests/smoke.py` comprueba la instalación, reinstalación y desinstalación con un `HOME` temporal; también inicia un servidor tmux aislado.

## Dependencias y créditos

Las fuentes de tmux-sessionx, tmux-floax, tmux-resurrect y tmux-thumbs se distribuyen con sus respectivas licencias. Consulta [THIRD_PARTY.md](THIRD_PARTY.md) para las versiones, modificaciones y enlaces. La configuración propia está bajo [MIT](LICENSE); las licencias de terceros se mantienen por separado.

## English

A macOS Ghostty/tmux/zsh setup with Tokyo Night styling and Kitty-inspired shortcuts. Install with `./install.sh --install-deps`; add `--without-thumbs` to skip Rust and tmux-thumbs. The installer backs up replaced files. Run `./install.sh --uninstall` to undo the most recent installation. Apple Silicon has been tested; Intel and Linux remain unverified.
