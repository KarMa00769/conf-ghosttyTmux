# Componentes de terceros

Los directorios bajo `templates/ghostty/plugins/` incluyen las licencias originales de cada proyecto. Los identificadores son los commits registrados en la instalación de origen; se incluyen instantáneas de código fuente, sin binarios compilados.

| Proyecto | Origen | Commit de referencia | Licencia incluida |
| --- | --- | --- | --- |
| tmux-sessionx | https://github.com/omerxx/tmux-sessionx | `8df6df56639acedb5343a6db02cf58120ff09ef7` | GPL-3.0 |
| tmux-floax | https://github.com/omerxx/tmux-floax | `133f526793d90d2caa323c47687dd5544a2c704b` | GPL-3.0 |
| tmux-resurrect | https://github.com/tmux-plugins/tmux-resurrect | `cff343cf9e81983d3da0c8562b01616f12e8d548` | MIT |
| tmux-thumbs | https://github.com/fcsonline/tmux-thumbs | `ae91d5f7c0d989933e86409833c46a1eca521b6a` | MIT |

Floax contiene adaptaciones locales en `scripts/utils.sh`: se ajustaron rutas y se evitaron modificaciones globales de atajos. Sessionx y Thumbs incluyen ajustes de comillas para rutas con espacios; el lanzador de Floax y Sessionx evita avisos al iniciar tmux antes de crear una sesión. Los atajos de prefijo se corrigen en la configuración tmux del proyecto. Las integraciones de Starship y Zoxide bajo `nushell/` se generaron a partir de sus respectivas herramientas; sus proyectos originales son [Starship](https://github.com/starship/starship) y [Zoxide](https://github.com/ajeetdsouza/zoxide).

Las licencias para las integraciones generadas se conservan en [`licenses/`](licenses/): Starship (ISC), Zoxide (MIT) y Carapace (MIT).
