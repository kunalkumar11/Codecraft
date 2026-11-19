<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-dark.png">
    <img src="../assets/logo.png" width="220" alt="CodeCraft, el senior dev perezoso">
  </picture>
</p>

<h1 align="center">CodeCraft</h1>

<p align="center">
  <em>No dice nada. Escribe una línea. Funciona.</em>
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/50668?utm_source=repository-badge&utm_medium=badge&utm_campaign=badge-repository-50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/repositories/50668" alt="kunalkumar11%2FCodecraft | Trendshift" width="250" height="55"/></a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/kunalkumar11/Codecraft?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/github/v/release/kunalkumar11/Codecraft?style=flat-square&color=111111&label=release" alt="Release">
  <img src="https://img.shields.io/npm/v/@kunalkumar11/codecraft?style=flat-square&color=111111&label=npm" alt="npm">
  <img src="https://img.shields.io/badge/works%20with-20%20agents-111111?style=flat-square" alt="Works with 20 agents">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <a href="https://trendshift.io/repositories/50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/daily" alt="kunalkumar11/Codecraft | Trendshift" width="250" height="55"/></a>
  <a href="https://trendshift.io/repositories/50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/weekly" alt="kunalkumar11/Codecraft | Trendshift" width="250" height="55"/></a>
  <a href="https://trendshift.io/repositories/50668?utm_source=trendshift-badge&utm_medium=badge&utm_campaign=badge-trendshift-50668" target="_blank" rel="noopener noreferrer"><img src="https://trendshift.io/api/badge/trendshift/repositories/50668/monthly?language=JavaScript" alt="kunalkumar11%2FCodecraft | Trendshift monthly ranking" width="250" height="55"/></a>
</p>

<p align="center">
  <img src="../assets/v5/hero-es.jpg" width="880" alt="CodeCraft 5, reconstruido desde cero: -53% código, -41% tiempo, -26% coste, -45% tokens. Y aun así el 98% de la lógica arriesgada sale con un test; sin CodeCraft, el 68%.">
</p>

<p align="center">
  <strong>CodeCraft 5: reconstruido desde cero.</strong><br>
  <strong>-53% código &middot; -41% tiempo &middot; -26% coste &middot; -45% tokens</strong><br>
  <strong>Y aun así: el 98% de la lógica arriesgada sale con un test.</strong> Sin CodeCraft: 68%.<br>
  <sub>Medido en Claude Code, el mismo agente con y sin el skill: 39 tareas, entre ellas un repo real de FastAPI + React, Opus 5.5, 5 ejecuciones cada una. <a href="#numbers">Detalles</a>.</sub>
</p>

<p align="center">
  <sub><a href="../README.md">English</a> &middot; Español &middot; <a href="README.ko.md">한국어</a> &middot; <a href="README.zh-CN.md">简体中文</a> &middot; <a href="README.ja.md">日本語</a></sub><br>
  <sub>Traducción del README en inglés. Si algo no coincide, vale la <a href="../README.md">versión en inglés</a>.</sub>
</p>

---

<p align="center">
  <a href="https://codecraft.dev/soon"><img src="../assets/waitlist-banner-es.png" alt="Algo se acerca, únete a la lista de espera" width="760"></a>
</p>

## Ya construido con CodeCraft

<a href="https://theretriever.app">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="../assets/retriever-logo-dark.svg">
    <img src="../assets/retriever-logo-light.svg" height="128" alt="Retriever">
  </picture>
</a>

---

Ya lo conoces. Coleta larga. Gafas ovaladas. Lleva en la empresa más tiempo que el control de versiones. Le enseñas cincuenta líneas; las mira, no dice nada y las cambia por una.

CodeCraft lo mete dentro de tu agente de IA.

<a id="numbers"></a>
## Números

<p align="center">
  <img src="../assets/v5/chart-es.png" width="880" alt="Porcentaje del baseline sin skill. Líneas de código: CodeCraft v4.13 52%, CodeCraft 5 47%. Tokens de salida: 57% y 55%. Coste: 84% y 74%. Tiempo: 62% y 59%.">
</p>

<p align="center">
  <img src="../assets/v5/tests-es.png" width="880" alt="La mitad del código, y aun así mejor: el 98% de la lógica arriesgada sale con un test (sin skill 68%); los propios tests del agente detectan el 66% de los bugs inyectados (sin skill 46%).">
</p>

Dos cosas que el gráfico no muestra: en una comparación a ciegas, las respuestas de CodeCraft 5 ganan a las del CodeCraft anterior por 110 a 67. Y en las seis tareas de seguridad (inyección SQL, path traversal, tokens falsificados, limitación de peticiones, filas CSV mal formadas, caché) pasó las 30 ejecuciones: menos código, igual de seguro. Método, tablas por tarea y limitaciones: [benchmarks/results/2026-10-07-agentic.md](../benchmarks/results/2026-10-07-agentic.md).

**La regla nunca fue "la menor cantidad de tokens".** Es: escribe solo lo que la tarea necesita, y nunca recortes validación, manejo de errores, seguridad ni accesibilidad. El código acaba siendo pequeño porque es lo necesario, no porque esté comprimido a la fuerza. El menor coste y la menor latencia son un efecto secundario.

## Antes / después

<p align="center">
  <img src="../assets/v5/beforeafter-es.png" width="880" alt="Añade un selector de fechas al frontend. Sin skill: 335 líneas, un calendario y un selector de fechas hechos a mano. CodeCraft 5: un archivo de 10 líneas que reutiliza el Input del repo con type date, y el navegador pone el calendario.">
</p>

Pides un selector de fechas. Sin CodeCraft, el agente instala una librería de selector de fechas o construye un calendario entero a mano: 335 líneas. CodeCraft 5 primero mira lo que ya hay: el repo tiene un componente `Input`, y todos los navegadores traen un selector de fechas. Junta las dos cosas. 10 líneas.

Más supervivientes en [examples/](../examples/).

## La revisión, reconstruida

<p align="center">
  <img src="../assets/v5/review-es.png" width="880" alt="La revisión, reconstruida. Un hallazgo real de /codecraft-review en el benchmark: el cambio renombró un campo, y un archivo que nadie tocó, src/routes/feed.js, ahora se cae. Hay que arreglarlo: el feed Atom ahora se cae en cada petición, con qué es esto, el problema, el arreglo y qué pasa si no se arregla. Encuentra el 100% de los problemas plantados, sin skill el 87%. Encuentra el 100% de los problemas fuera del diff, sin skill el 78%.">
</p>

`/codecraft-review` antes solo buscaba código que recortar. Ahora revisa como el dev senior al que llaman cuando algo se rompe: lee el código que toca tu cambio, no solo el diff, y revisa bugs, seguridad, carga real, tests que faltan, velocidad y lo que sobra. Cada hallazgo dice qué hace el código, qué falla, cómo arreglarlo y qué pasa si no lo arreglas.

## La auditoría, reconstruida

<p align="center">
  <img src="../assets/v5/audit-es.png" width="880" alt="Todo tu repo, por orden de prioridad. Arregla esto primero. Un /codecraft-audit real del benchmark sobre un repo de stock de almacén: 1 hay que arreglarlo, los lotes de oficina de 1200 fallan por completo; 2 hay que arreglarlo, la importación se salta en silencio las filas erróneas; 3 hay que arreglarlo, un SKU mal escrito en un lote de oficina se ignora en silencio; 4 conviene arreglarlo, las partes arriesgadas del código no tienen tests; 5 estaría bien, la API se cae con un body que no es un objeto. Veredicto: arregla primero el 1.">
</p>

`/codecraft-audit` hace las mismas comprobaciones en todo el repo. Primero hace un mapa del código: puntos de entrada, cómo se mueven los datos, qué carga espera el proyecto. Después ordena lo que encuentra por prioridad y te dice qué arreglar primero. La auditoría anterior solo listaba lo que había que borrar.

## Nuevo en 5.3: la barra

<p align="center">
  <img src="../assets/band/band.png" width="880" alt="La barra de CodeCraft en Claude Code, encima del prompt. Modo detalle: coste $23.80, último turno $1.14, media $0.72 por turno; 56.7M tokens, 168k de salida, 33 turnos; tiempo de agente 52m 14s; reutilización 71%, 5 usados, 2 nuevos; tests pasados después del último cambio. El modo compacto muestra lo mismo en una línea.">
</p>

En Claude Code, CodeCraft ahora muestra una barra encima del prompt: cuánto cuesta la tarea actual, cuántos tokens y cuánto tiempo de agente ha usado, cuántas veces reutilizó código existente en lugar de escribir código nuevo y si los tests pasaron después del último cambio. Sus botones cambian el nivel, lanzan `/codecraft-review` o `/codecraft-audit`, copian la tarea como Markdown y pliegan la barra en una sola línea. ¿No la quieres? `/codecraft band` la oculta, y el mismo comando la vuelve a mostrar. Necesita Claude Code 2.1.290 o posterior, en la terminal o en la app de escritorio. No aparece en el panel de chat de VS Code, en sesiones en la nube ni con `claude -p`.

<p align="center">
  <img src="../assets/band/board.png" width="880" alt="El board de CodeCraft, una página local: 61 sesiones, 20h 13m de tiempo de agente, $285.30 y 492.5M tokens en los últimos 30 días; tiempo de agente por proyecto a lo largo del tiempo; las últimas sesiones con sus tests; días activos y racha.">
</p>

**Board** abre una página local con todas las tareas de tus proyectos: coste, tiempo de agente y tokens a lo largo del tiempo, cada sesión con sus tests y los días que trabajaste. Por defecto, todo se queda en tu máquina, en `~/.config/codecraft/band/`. `/codecraft band import` añade tus sesiones anteriores de Claude Code al board, con su coste, tiempo de agente y tokens.

## Cómo funciona

<p align="center">
  <img src="../assets/v5/ladder-es.png" width="880" alt="Antes de escribir código, detente en el primer peldaño que se sostiene: 1 ¿hace falta que exista?, 2 ¿ya está en este código?, 3 ¿lo hace la librería estándar?, 4 una función nativa de la plataforma, 5 una dependencia instalada, 6 ¿puede ser una línea?, 7 solo entonces lo mínimo que funcione, más un test pequeño si tiene lógica.">
</p>

La escalera corre *después* de entender el problema, no en su lugar: lee el código que toca el cambio y sigue el flujo real antes de elegir un peldaño. Perezoso con la solución, nunca con la lectura.

Perezoso, no negligente: la validación en los límites de confianza, el manejo de pérdida de datos, la seguridad y la accesibilidad nunca se recortan.

La lógica con una rama, un bucle, un parser, dinero o seguridad deja un test pequeño. Cada respuesta termina con lo que se saltó o no se comprobó y cualquier riesgo que debas conocer.

## El prompt

CodeCraft es un solo prompt: [`skills/codecraft/SKILL.md`](../skills/codecraft/SKILL.md). La versión compacta, para agentes que leen un archivo de reglas, es [`AGENTS.md`](../AGENTS.md). Todo lo demás en este repo sirve para cargar ese prompt en distintos agentes.

## Instalación

**Claude Code**, como dos prompts separados:

```
/plugin marketplace add kunalkumar11/Codecraft
```
```
/plugin install codecraft@codecraft
```

**Codex:**

```bash
codex plugin marketplace add kunalkumar11/Codecraft
codex plugin add codecraft@codecraft
```

Después abre `/hooks` en Codex, confía en sus dos hooks de ciclo de vida y empieza un hilo nuevo.

**Cualquier otro agente:** copia [`AGENTS.md`](../AGENTS.md) en tu proyecto, o pídele a tu agente que instale [`skills/codecraft/SKILL.md`](../skills/codecraft/SKILL.md) como skill. Paso a paso para Copilot, Cursor, OpenCode, Gemini y el resto (en inglés): **[INSTALL.md](../INSTALL.md)**.

Eso era todo. Estaría orgulloso. No lo va a decir.

Activo en cada sesión, con un puñado de comandos (ver [Comandos](#commands)). `/codecraft ultra` existe para cuando el código te ha ofendido personalmente. El texto de inicio y de cambio de modo muestra el modo actual.

Instala CodeCraft solo desde `kunalkumar11/Codecraft` en GitHub o `@kunalkumar11/codecraft` en npm. Nunca incluye archivos `.exe` ni `.dll`; una copia que los incluya no es mía.

<a id="commands"></a>
## Comandos

| Comando | Qué hace |
|---------|----------|
| `/codecraft [lite \| full \| ultra \| off]` | Ajusta la intensidad o lo apaga. Sin argumento enciende CodeCraft en el nivel por defecto si está apagado; si no, muestra el nivel actual. |
| `/codecraft band [on \| off]` | Solo en Claude Code: oculta o muestra la barra encima del prompt. Sin argumento la alterna. El nivel no cambia. |
| `/codecraft band import` | Solo en Claude Code: añade tus sesiones anteriores al board, con coste, tiempo de agente y tokens. |
| `/codecraft-review` | Revisa el diff actual como el dev senior al que llaman cuando algo se rompe: bugs, seguridad, carga real, código arriesgado sin test, partes lentas y lo que sobra. Cada hallazgo dice qué hace el código, qué falla, cómo arreglarlo y qué pasa si no se arregla. Indica un objetivo con palabras normales para acotarlo o ampliarlo: `uncommitted`, `staged`, `branch` o un enlace a un PR. |
| `/codecraft-audit` | La misma revisión para todo el repo, lo más importante primero. |
| `/codecraft-debt` | Reúne los atajos `shortcut:` que dejaste para después en un registro, para que "luego" no se convierta en "nunca". |
| `/codecraft-gain` | Muestra el marcador de impacto medido (menos código, menos coste, más velocidad) del benchmark. |
| `/codecraft-help` | Referencia rápida de los comandos anteriores. |

Los comandos necesitan un host con soporte de skills (Claude Code, Codex, Devin CLI, OpenCode, Gemini, Antigravity CLI, pi, Hermes Agent, Qoder, Grok Build). En Codex CLI y en la extensión del IDE son skills dentro del espacio de nombres del plugin; se invocan con `$codecraft:codecraft-review`. Cursor con los [hooks](../INSTALL.md#cursor) solo tiene el cambio de nivel con `/codecraft`, escrito como mensaje normal. Los adaptadores de solo instrucciones (el archivo de reglas de Cursor, Windsurf, Cline, Copilot, Kiro, el modo alternativo de Antigravity con `AGENTS.md`) cargan las reglas siempre activas, sin los comandos.

## Preguntas frecuentes

**¿Necesita un archivo de configuración?**
No. Un `~/.config/codecraft/config.json` opcional o la variable de entorno `CODECRAFT_DEFAULT_MODE` pueden fijar el nivel por defecto, pero no hace falta nada.

**¿Por qué escribe comentarios `shortcut:`?**
Marcan un atajo deliberado y cuándo revisarlo, y `/codecraft-debt` los reúne en un registro. ¿Quieres otra palabra, o ninguna? Dilo en el `CLAUDE.md` o `AGENTS.md` de tu proyecto y luego ejecuta `/codecraft-debt <tu palabra>`.

**¿Y si de verdad necesito la clase de caché de 120 líneas?**
No la necesitas. Insiste de todos modos y te la construye. Despacio. Correctamente. Mirándote.

**¿Escala?**
El código que nunca escribiste escala hasta el infinito. Cero bugs, cero CVEs, 100% de disponibilidad desde siempre.

**¿Por qué "CodeCraft"?**
Sabes perfectamente por qué.

## Patrocinadores

<p align="center">
  <a href="https://greenpt.com/">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="../assets/logo-greenpt-dark.svg">
      <img src="../assets/logo-greenpt.svg" width="260" alt="GreenPT">
    </picture>
  </a>
</p>

## Licencia

[MIT](../LICENSE). La licencia más corta que funciona.

## Historial de estrellas

<a href="https://www.star-history.com/kunalkumar11/Codecraft#history">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=kunalkumar11/Codecraft&type=Date" />
 </picture>
</a>