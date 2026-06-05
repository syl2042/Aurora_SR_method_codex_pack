# Aurora SR Method Codex Pack

[English](README.md) |
[Francais](README.fr.md) |
[Deutsch](README.de.md) |
[Portugues](README.pt.md) |
[Espanol](README.es.md)

[Dar una estrella al repositorio](https://github.com/syl2042/Aurora_SR_method_codex_pack/stargazers) |
[Documentación](https://docs.auroramind.fr/docs/SR_Method) |
[Instalar con Codex](INSTALLATION.es.md) |
[Actualizar proyecto](prompts/es/05_upgrade_codex_environment.md) |
[Verificar instalación](prompts/es/06_verify_sr_installation.md)

## Qué es

Aurora SR Method Codex Pack es un paquete fuente público para instalar un método de trabajo Codex gobernado en proyectos de software.

SR significa **Specification Runtime**. El método proporciona a Codex un marco operativo local al proyecto: reglas de bootstrap, plantillas de memoria de tarea, evidence gates, repo maps, prompts controlados, scripts de validación y method skills reutilizables.

```text
Clonar paquete -> Pegar prompt Codex -> Instalar SR Method -> Verificar -> Desarrollar con gobernanza
```

## Por qué lo usan los desarrolladores

La SR Method está diseñada para desarrolladores que quieren que Codex trabaje como un compañero de proyecto disciplinado, no como un generador de código puntual.

Convierte solicitudes amplias en sesiones de desarrollo controladas, con alcance explícito, memoria de tarea escrita, decisiones basadas en evidencias, gates de validación y handoffs limpios.

Beneficios principales para desarrolladores:

- **Onboarding de proyecto más rápido**: Codex lee el repositorio, detecta la stack e instala un marco operativo local al proyecto.
- **Menos pérdida de contexto**: memoria de tarea, estado actual, hallazgos, decisiones y notas de verificación se escriben dentro del proyecto.
- **Trabajo autónomo más seguro**: Codex trabaja por lots limitados, verifica evidencias antes de cambiar código y mantiene explícita la validación humana.
- **Mejor continuidad entre sesiones**: otra sesión Codex u otro desarrollador puede retomar desde el estado escrito.
- **Reviews más claras**: los cambios quedan vinculados al alcance, hipótesis, archivos tocados, comandos de verificación y riesgos restantes.
- **Disciplina operativa reutilizable**: el mismo método puede instalarse en varios proyectos, adaptándose a cada repositorio.
- **Flujo prompt-first**: los desarrolladores interactúan con Codex mediante prompts copiables; los scripts siguen siendo detalles de ejecución usados por Codex cuando corresponde.

En la práctica, el pack reduce el coste de dar trabajo real de proyecto a Codex: menos cambios vagos, menos restricciones olvidadas, validación más clara y mejores handoffs.

## Política de idioma

El núcleo de la SR Method se mantiene en inglés como idioma técnico canónico.

Los puntos de entrada para desarrolladores están disponibles en varios idiomas: README, guías de instalación y prompts Codex copiables.

Un proyecto instalado puede indicar a Codex que hable con el usuario en español. El núcleo técnico permanece en inglés.

## Inicio rápido

1. Clona este repositorio.
2. Abre Codex en el proyecto destino.
3. Pega el prompt de instalación en español.
4. Deja que Codex inspeccione, instale, verifique y reporte.

Prompts principales:

| Acción | Prompt |
| --- | --- |
| Instalar | [00](prompts/es/00_install_codex_environment.md) |
| Iniciar sesión | [01](prompts/es/01_start_sr_session.md) |
| Actualizar | [05](prompts/es/05_upgrade_codex_environment.md) |
| Verificar | [06](prompts/es/06_verify_sr_installation.md) |
| Definir agentes runtime | [15](prompts/es/15_define_runtime_agents.md) |

Los comandos Python son herramientas técnicas o fallback. El flujo recomendado es prompt-first con Codex.

## Contenido público

```text
core/             núcleo canónico en inglés y plantillas
prompts/          prompts raíz y entradas multilingües
scripts/          instalación, auditoría y validación
skills-method/    method skills Codex reutilizables
blueprints/       plantillas de lots, inbox, tasks y skills
profiles/         perfiles genéricos
project-skills/   espacio para skills locales del proyecto
adr/              plantilla ADR
```

El repositorio público no publica estado de proyecto, tasks históricas, `.docx`, handoffs locales, rutas de clientes ni datos de proyectos.

## Licencia

MIT License. Ver [LICENSE](LICENSE).
