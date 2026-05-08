Autor: Alan Sastre

GitHub: [github.com/alansastre/genai-asistentes-codigo](https://github.com/alansastre/genai-asistentes-codigo)

Las **extensiones de IA para IDEs** son plugins que añaden capacidades de inteligencia artificial a editores de código existentes como Visual Studio Code o los productos de JetBrains. Representan la forma más accesible de incorporar asistencia de IA al flujo de trabajo de desarrollo, ya que permiten mantener el entorno habitual mientras se añaden funcionalidades avanzadas de generación y comprensión de código.

A diferencia de los IDEs con IA nativa como Cursor o Windsurf, las extensiones no requieren cambiar de editor. Esto facilita su adopción en equipos con flujos de trabajo establecidos y reduce la curva de aprendizaje.

## Panorama de extensiones de IA para IDEs

| Extensión | Proveedor | Enfoque |
|-----------|-----------|---------|
| [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot) | GitHub | Autocompletado, chat y modo agente |
| [OpenAI Codex](https://openai.com/blog/openai-codex/) | OpenAI | Agente y revisión de código |
| [Claude Code for VS Code](https://claude.ai/code) | Anthropic | Razonamiento profundo y contexto amplio |
| [Google Gemini Code Assist](https://codeassist.google/) | Google | Integración con GCP y edición asistida |
| [Amazon Q](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.amazon-q-vscode) | AWS | Seguridad y transformación de código |
| [JetBrains AI Assistant](https://www.jetbrains.com/ai/) | JetBrains | Integración nativa con IDEs JetBrains |

### GitHub Copilot

[Marketplace](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)

Desarrollada por GitHub en colaboración con OpenAI, es la extensión con **mayor adopción** en la industria. Su integración con el ecosistema GitHub la convierte en la opción natural para equipos que trabajan en esta plataforma.

Características distintivas:

- **Copilot Chat** con slash commands (/explain, /fix, /tests, /doc)
- **Agent Mode** para ejecución autónoma de tareas multi-archivo
- **Vision** para convertir imágenes, mockups y diagramas en código
- **Prompt Files** (.github/copilot-instructions.md) para instrucciones reutilizables
- **Coding Agent** asíncrono que trabaja en segundo plano sobre issues de GitHub
- Soporte **multi-modelo**.

> GitHub Copilot ha evolucionado de un asistente de autocompletado a un sistema agéntico completo, con capacidad de crear pull requests de forma autónoma a partir de issues asignados.

**Ecosistema:** GitHub Actions, Pull Requests, Issues, Codespaces y GitHub Security.

### OpenAI Codex

[Web oficial](https://openai.com/blog/openai-codex/)

Extensión oficial de OpenAI que proporciona acceso directo a los modelos optimizados para código, incluyendo las últimas versiones de GPT.

Características distintivas:

- **Tres modos de operación**: Chat, Agent y Agent Full Access
- **Codex Cloud** para delegación de tareas en infraestructura remota
- **Revisión de código** automática mediante menciones @codex en PRs
- **Compatibilidad** con VS Code y forks como Cursor y Windsurf
- **Sincronización** entre dispositivos a través de la cuenta de OpenAI

**Ecosistema:** Plataforma OpenAI, integración con GitHub para revisiones automáticas.

### Claude Code for VS Code

[Web oficial](https://claude.ai/code)

Extensión de Anthropic que integra los modelos Claude directamente en Visual Studio Code. Destaca por las capacidades de razonamiento extendido y la comprensión profunda de bases de código complejas.

Características distintivas:

- **Lanzamiento rápido** con Cmd+Esc (macOS) / Ctrl+Esc (Windows/Linux)
- **Vista de diffs nativa** integrada con el visor de diferencias de VS Code
- **Compartir diagnósticos** con envío automático de errores del linter
- **Sincronización con CLI** para alternar entre la extensión y Claude Code en terminal
- **Ventana de contexto extendida** para proyectos de gran tamaño

**Ecosistema:** Integración bidireccional con Claude Code CLI y la plataforma Anthropic.

### Google Gemini Code Assist

[Gemini Code Assist](https://codeassist.google/)

Acceso a los modelos Gemini de Google con funcionalidades orientadas a equipos que utilizan Google Cloud Platform.

Características distintivas:

- **Agent Mode** que actúa como par programador para tareas complejas
- **Next Edit Predictions** para anticipar la siguiente modificación
- **Comandos personalizados** para automatizar tareas repetitivas
- **Reglas de proyecto** para definir convenciones que el modelo debe seguir
- **Context Drawer** para control granular del contexto enviado al modelo

**Ecosistema:** Google Cloud Platform, Firebase, BigQuery y servicios de GCP.

### Amazon Q

[Amazon Q](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.amazon-q-vscode)

Extensión de AWS que combina asistencia de código con soporte especializado para servicios cloud de Amazon. Incluye capacidades de seguridad y transformación de código.

Características distintivas:

- **Transformación de código** para actualizar versiones de lenguajes y frameworks
- **Escaneo de seguridad** con detección de vulnerabilidades y remediaciones
- **Documentación automática** incluyendo READMEs y diagramas arquitectónicos
- **Soporte MCP nativo** para integrar herramientas externas
- **Personalización** con repositorios internos de la organización

**Ecosistema:** AWS Lambda, DynamoDB, S3, EC2 y el resto de servicios de AWS.

### JetBrains AI Assistant

[Web oficial](https://www.jetbrains.com/ai/)

Integrado nativamente en todos los IDEs de JetBrains (IntelliJ IDEA, PyCharm, WebStorm, etc.), aprovecha las capacidades avanzadas de análisis estático y refactorización de estos entornos.

Características distintivas:

- **Modelo Mellum** propio de JetBrains, optimizado para tareas de código
- **Modelos locales** mediante conexión con Ollama, LM Studio o llama.cpp
- **Chat con imágenes** para describir interfaces o diagramas
- **Junie** como agente autónomo integrado en el chat
- **Next Edit Suggestions** combinando IA con acciones determinísticas del IDE

**Ecosistema:** Refactorización avanzada, inspecciones de código y herramientas propias de JetBrains.
