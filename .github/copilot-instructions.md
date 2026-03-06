# AI Agent Instructions for genai-devtools

## Project Overview
Educational repository exploring the landscape of AI-powered development tools and their implementation. Focuses on:
- Survey and comparison of AI coding assistants (GitHub Copilot, Cursor, Claude Code)
- Setup guides and practical examples for each tool
- Educational modules delivered via Jupyter notebooks
- Demonstration projects showcasing integration patterns

## Repository Structure
```
01-landscape/        # Market analysis and taxonomy of AI dev tools
  ├── 01-introduccion.ipynb       → Evolution of AI in development + tool taxonomy
  ├── 02-extensiones-ide.ipynb    → IDE extensions (Copilot, Claude, etc.)
  ├── 03-ides.ipynb               → Native AI IDEs (Cursor, Windsurf, etc.)
  ├── 04-clis.ipynb               → CLI agents and terminal interfaces
  ├── 05-cloud-agents.ipynb       → Cloud-based agents (Devin, Jules)
  └── 06-contexto-para-agentes.ipynb → Context provision & MCP servers

02-github-copilot/   # GitHub Copilot setup and usage examples
  ├── 01-setup.ipynb              → Installation, authentication, activation
  ├── 02-completions.ipynb        → Inline code suggestions patterns
  ├── 02-models.py                → Reference models (Company, Employee, Project)
  └── 03-chat.ipynb               → Chat interface and conversation patterns

03-cursor/           # Cursor IDE exploration (WIP)
04-claude-code/      # Claude Code CLI integration (WIP)
05-proyecto/         # Practical project implementations (empty)
```

## Key Content Patterns

### Notebooks Are Educational, Not Production Code
- All `.ipynb` files are **teaching materials** with markdown explanations
- Notebooks document setup procedures, not software workflows
- Markdown cells contain the primary content (code is illustrative)
- Code examples in notebooks demonstrate concepts, not production patterns

### Example Models in `02-models.py`
Simple data models demonstrating class relationships:
- `Company`: Basic entity with name, industry, employee count
- `Employee`: With full_name property and email validation
- `Project`: Many-to-many relationship with employees (list-based)

These are **conceptual references** for educational discussion, not production data layers.

### Documentation Language
Content is in **Spanish** (es) with some technical English terms. When expanding content:
- Maintain Spanish for explanatory text
- Use English for code and technical terms
- Match the teaching style: progressive, hands-on, example-driven

## Development Workflows

### Adding Educational Content
1. Create markdown cells explaining concepts with diagrams (mermaid recommended)
2. Add code examples in subsequent code cells (optional, if needed for clarity)
3. Reference files in the codebase as examples when illustrating patterns
4. Structure notebooks with clear sections (H2 headers) and learning progression

### Expanding to Active Project Work
When moving beyond educational content to `05-proyecto/`:
- Define clear project scope in README
- Use Python with type hints (demonstrated in `02-models.py`)
- Model relationships explicitly (Company→Employee, Employee→Project pattern)
- Include docstrings explaining business logic

### Documentation Standards
- Use mermaid flowcharts for workflows and decision trees
- Reference official tool documentation with direct links
- Include subscription/pricing information when relevant
- Add troubleshooting sections for setup guides

## Integration Points & Dependencies

### External Tools Referenced
- **GitHub Copilot**: VS Code native integration (no plugin needed)
- **Cursor IDE**: Standalone IDE with built-in AI
- **Claude Code**: CLI tool for AI-assisted coding
- **VS Code**: Primary editor platform for examples

### Context & Authentication
- GitHub account required for Copilot activation
- Three subscription tiers: Free (2k inline suggestions/mo), Pro ($10/mo), Pro+ ($39/mo)
- Free plan sufficient for exploration and learning
- Telemetry disabled via `telemetry.telemetryLevel: off` setting

## Conventions & Patterns to Follow

### Class Design
- Use type hints in `__init__` signatures
- Implement `__repr__` for debugging visibility
- Add properties for computed attributes (see `full_name` in Employee)
- Include simple validation methods (e.g., `validate_email()`)

### Comments & Documentation
- Spanish explanatory text with English for code
- Mark conceptual contributions with "Nueva clase..." comments
- Keep code comments brief; rely on class names and property names for clarity

### File Organization
- One notebook per major topic within a section
- Name notebooks numerically (`01-`, `02-`) for ordering
- Reference external links with inline markdown
- Use tables for comparisons (e.g., subscription plans)

## Key Files to Reference When Making Changes
- [01-landscape/01-introduccion.ipynb](01-landscape/01-introduccion.ipynb) → Defines tool categories and taxonomy
- [02-github-copilot/01-setup.ipynb](02-github-copilot/01-setup.ipynb) → Template for setup documentation
- [02-github-copilot/02-models.py](02-github-copilot/02-models.py) → Class design patterns used in the project

## Additional Context
- **Target Audience**: Developers learning about AI-assisted development tools
- **Scope**: Educational + exploratory (not production-focused)
- **Update Frequency**: Add new tool explorations as ecosystem evolves
- **Maintenance**: Keep tool links and subscription prices current
