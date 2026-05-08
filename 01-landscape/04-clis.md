Autor: Alan Sastre

GitHub: [github.com/alansastre/genai-asistentes-codigo](https://github.com/alansastre/genai-asistentes-codigo)

Los **agentes de terminal** son herramientas de línea de comandos que integran modelos de lenguaje directamente en el flujo de trabajo del desarrollador. Permiten interactuar con la IA sin abandonar la terminal, ejecutar tareas complejas de forma autónoma y automatizar procesos mediante scripts.

Esta categoría incluye CLIs especializados de los principales **proveedores de modelos**, terminales completas rediseñadas con IA nativa y herramientas open source. Al igual que ocurre con los IDEs, las funcionalidades tienden a converger: todos ofrecen chat interactivo, ejecución de comandos, edición de archivos y soporte para MCP.

## Panorama de agentes de terminal

El mercado de agentes de terminal experimentó una expansión significativa en 2025, cuando los principales proveedores de modelos lanzaron sus propias herramientas CLI para competir directamente con soluciones establecidas.

| Herramienta | Proveedor | Lanzamiento | Innovación distintiva |
|-------------|-----------|-------------|----------------------|
| [WARP](https://www.warp.dev) | Warp | Abril 2023 | Terminal completa rediseñada con IA nativa |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Anthropic | Febrero 2025 | Subagentes personalizables y Plan Mode |
| [Codex CLI](https://github.com/openai/codex) | OpenAI | Abril 2025 | Open source con Codex Cloud |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | Google | Junio 2025 | Open source con 1M tokens de contexto |
| [Copilot CLI](https://github.com/github/copilot-cli) | GitHub | Septiembre 2025 | Integración nativa con GitHub |
| [Kiro CLI](https://kiro.dev) | AWS | Noviembre 2025 | Integración nativa con servicios AWS |
| [OpenCode](https://opencode.ai) | Open Source | 2025 | Agnóstico del modelo, TUI nativa |

### WARP

**WARP** fue fundada en junio de 2020 y lanzó su integración de IA en **abril de 2023**, siendo pionera en el concepto de terminal con IA nativa. A diferencia del resto de herramientas de esta lista, WARP no es un CLI que se instala en una terminal existente, sino una **terminal completa rediseñada** como entorno de desarrollo agéntico.

Su propuesta diferencial es la experiencia de usuario: interfaz basada en bloques que organiza comandos y salidas en secciones diferenciadas, autosugerencias proactivas basadas en errores e historial, y **Ambient Agents** que trabajan en segundo plano monitorizando la actividad. En febrero de 2025 lanzó soporte oficial para Windows, completando su disponibilidad multiplataforma.

### Claude Code

**Claude Code** fue anunciado el **24 de febrero de 2025** junto con el modelo Claude 3.7 Sonnet. Anthropic lo posicionó como una herramienta para delegar tareas de ingeniería completas directamente desde la terminal.

Su característica más distintiva son los **subagentes personalizables**: el desarrollador puede definir agentes especializados en archivos Markdown con roles específicos (revisor de código, ejecutor de tests, especialista en depuración). También introdujo el concepto de **Plan Mode**, un modo de solo lectura para explorar y planificar cambios antes de ejecutarlos. En octubre de 2025 se expandió con Claude Code on the web, permitiendo ejecutar tareas en infraestructura cloud de Anthropic.

### OpenAI Codex CLI

**Codex CLI** fue lanzado el **16 de abril de 2025** como proyecto **open source**. OpenAI apostó por construir la herramienta en Rust para alto rendimiento y publicar el código bajo licencia abierta, diferenciándose de su competencia directa.

Su propuesta distintiva fue **Codex Cloud**: la capacidad de delegar tareas a infraestructura remota de OpenAI, con sincronización automática de cambios al proyecto local. También incluye entrada multimodal, aceptando capturas de pantalla y diagramas como parte del contexto de las tareas.

### Gemini CLI

**Gemini CLI** fue lanzado el **25 de junio de 2025** como proyecto **open source** bajo licencia Apache 2.0. Google siguió una estrategia similar a OpenAI, publicando el código de forma abierta para fomentar adopción.

Su ventaja competitiva principal es la **ventana de contexto de 1 millón de tokens** de Gemini, que permite trabajar con proyectos completos sin fragmentar el contexto. También incluye Google Search grounding para fundamentar respuestas con búsquedas en tiempo real y routing inteligente que selecciona automáticamente el modelo óptimo según la complejidad de cada tarea.

### GitHub Copilot CLI

**GitHub Copilot CLI** entró en public preview el **25 de septiembre de 2025**. GitHub lo diseñó como reemplazo de la anterior extensión para GitHub CLI, ofreciendo un agente completo en lugar de comandos aislados.

Su diferenciación natural es la **integración nativa con el ecosistema GitHub**: acceso directo a repositorios, issues, pull requests y workflows de Actions. Permite tanto modificar código local como operar sobre GitHub.com, combinando tareas de desarrollo con gestión del repositorio en una única interfaz.

### Kiro CLI

**Kiro CLI** se lanzó junto con el IDE Kiro, alcanzando disponibilidad general en **noviembre de 2025**. Anteriormente conocido como Amazon Q Developer CLI, representa la apuesta de AWS por herramientas de desarrollo con IA.

Su propuesta diferencial es la **integración nativa con servicios AWS**: análisis de templates CloudFormation, gestión de recursos cloud y conexión directa con el ecosistema de Amazon. Comparte con el IDE Kiro el enfoque de desarrollo guiado por especificaciones.

### OpenCode

**OpenCode** es un proyecto **open source** que ha acumulado más de 80.000 estrellas en GitHub. A diferencia de las herramientas de proveedores comerciales, OpenCode es **agnóstico del modelo**: soporta más de 75 proveedores de LLMs incluyendo modelos locales via Ollama.

Su característica distintiva es la combinación de **privacidad** (no almacena código ni contexto en servidores externos) con una interfaz TUI nativa completa. Es la opción preferida para desarrolladores que trabajan en entornos con requisitos de seguridad estrictos o que prefieren usar modelos locales.

## Convergencia funcional

Todas estas herramientas han convergido hacia un conjunto de funcionalidades común: chat interactivo, ejecución de comandos shell, lectura y edición de archivos, modos de aprobación configurables y soporte para MCP. Las diferencias se encuentran en la **integración con ecosistemas específicos** (GitHub, AWS, Google Cloud), los modelos disponibles por defecto y matices de la experiencia de usuario.

La elección entre una u otra depende principalmente del proveedor de modelos preferido, la integración con servicios cloud existentes y consideraciones de privacidad (herramientas open source vs comerciales).
