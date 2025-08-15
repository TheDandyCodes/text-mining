# Information Discovery in Texts
To be Done

# Project Setup with uv and VSCode (Python + LLMs)

This repository uses [uv](https://github.com/astral-sh/uv) for Python environment and dependency management, ensuring speed and reproducibility.

## 1. Installing uv

You can install **uv** with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or using `pip`:

```bash
pip install uv
```

This will add the `uv` command to your terminal.

---

## 2. Initialize the project

In the repository root folder:

```bash
uv init .
```

This will create:
- `pyproject.toml` (project configuration)
- `.gitignore`
- `.venv` (virtual environment)
- Git initialization if it doesn't exist

You can also create a new project by specifying a name:

```bash
uv init my_llm_project
```

---

## 3. Adding dependencies

To install LLM libraries, for example **PyTorch** and **Transformers**:

```bash
uv add torch transformers
```

For development dependencies (formatting, testing, typing):

```bash
uv add --dev ruff pytest mypy
```

This will lock dependencies in `uv.lock` for reproducibility.

---

## 4. VSCode Configuration

Recommended extensions to install:
- **Python** (Microsoft)
- **Ruff**
- **Jupyter** (if using notebooks)

If VSCode doesn't automatically detect `.venv`:
- Press `Ctrl+Shift+P` → "Python: Select Interpreter" → select the one from `.venv`.

Configure `.vscode/settings.json`:

```json
{
"python.testing.pytestEnabled": true,
"python.testing.pytestArgs": ["tests"],
"editor.formatOnSave": true,
"[python]": {
"editor.defaultFormatter": "charliermarsh.ruff"
}
}
```

---

## 5. Makefile Commands

This project includes a `Makefile` with convenient commands for setup and maintenance:

### Available Commands

```bash
# Complete project setup (install uv + pre-commit hooks)
make install

# Run all pre-commit hooks on all files
make hooks

# Update pre-commit hook versions
make hooks-update
```

### Command Details

- **`make install`**:
  - Downloads and installs `uv` if not already present
  - Installs pre-commit hooks for code quality checks
  - Sets up the development environment automatically

- **`make hooks`**:
  - Runs all configured pre-commit hooks on every file in the repository
  - Useful for checking code quality across the entire project

- **`make hooks-update`**:
  - Updates all pre-commit hooks to their latest versions
  - Recommended to run periodically to keep tools up-to-date

### Usage Example

After cloning the repository, simply run:
```bash
make install
```

This single command will set up your entire development environment!

---

## 6. Pre-commit Hooks: Calidad de Código Automática

### ¿Qué son los hooks y pre-commit?

Los **hooks** son scripts que se ejecutan automáticamente en ciertos momentos de Git (antes de commit, push, etc.). **Pre-commit** es una herramienta que facilita su configuración y uso.

**Piénsalo así**: Antes de guardar tu código en Git, pre-commit automáticamente:
- ✅ Formatea tu código (lo hace bonito y consistente)
- ✅ Encuentra errores comunes
- ✅ Ordena imports
- ✅ Elimina espacios innecesarios
- ✅ Verifica sintaxis de archivos

### Configuración paso a paso

#### Paso 1: Instalar pre-commit
```bash
# Instalar pre-commit como dependencia de desarrollo
uv add --dev pre-commit ruff
```
Esto instala las herramientas pero **aún no las activa** en tu repositorio.

#### Paso 2: Crear archivo de configuración
Necesitas crear `.pre-commit-config.yaml` en la raíz del proyecto:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.9
    hooks:
      - id: ruff              # Linter
      - id: ruff-format       # Formateador
```
Este archivo le dice a pre-commit **qué verificaciones hacer**.

#### Paso 3: Activar los hooks en Git
```bash
uv run pre-commit install
```
**¿Por qué este comando?**
- Crea un archivo especial en `.git/hooks/pre-commit`
- Este archivo se ejecuta automáticamente **antes de cada commit**
- Sin este paso, pre-commit NO funciona automáticamente

**Nota**: En este proyecto ya está todo configurado. Solo necesitas clonar y usar.

### ¿Cómo funciona en la práctica?

#### Ejemplo 1: Commit normal
```bash
git add .
git commit -m "Mi cambio"

# 🔧 Pre-commit se ejecuta automáticamente:
# ✅ trim trailing whitespace...........Passed
# ✅ fix end of files...................Passed
# ✅ ruff...............................Passed
# ✅ ruff format........................Passed
# ✅ [main abc123] Mi cambio
```

#### Ejemplo 2: Cuando hay problemas
```bash
git add .
git commit -m "Código con errores"

# ❌ Pre-commit encuentra problemas:
# ❌ ruff...............................Failed
# - import unused detected
# - line too long detected
#
# ¡Git NO hace el commit hasta que se arreglen!
```

### Comandos útiles

```bash
# Ejecutar hooks manualmente en todos los archivos
uv run pre-commit run --all-files

# Ejecutar hooks solo en archivos específicos
uv run pre-commit run --files mi_archivo.py
```

### Herramientas incluidas (Ruff)

Este proyecto usa **Ruff**, una herramienta súper rápida que reemplaza:
- **Black** (formateo de código)
- **isort** (ordenamiento de imports)
- **flake8** (detección de errores)
- **pyupgrade** (modernización de código)

**Una sola herramienta = todo más simple y rápido** 🚀

### Configuración personalizable

Los hooks están configurados en:
- `.pre-commit-config.yaml` - Qué hooks ejecutar
- `pyproject.toml` - Configuración de Ruff

```yaml
# .pre-commit-config.yaml (simplificado)
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    hooks:
      - id: trailing-whitespace  # Elimina espacios extra
      - id: end-of-file-fixer   # Añade línea final

  - repo: https://github.com/astral-sh/ruff-pre-commit
    hooks:
      - id: ruff              # Linter (encuentra errores)
      - id: ruff-format       # Formateador (hace código bonito)
```

#### Estructura de archivos:
```
tu-proyecto/
├── .pre-commit-config.yaml     # ← Qué hooks ejecutar
├── .git/
│   └── hooks/
│       └── pre-commit          # ← Script que ejecuta Git (creado automáticamente)
└── pyproject.toml              # ← Configuración de Ruff
```

### Solución de problemas comunes

#### "Los hooks no se ejecutan automáticamente"
```bash
# Verificar si están instalados
ls .git/hooks/pre-commit

# Si no existe, instalarlos
uv run pre-commit install
```

#### "Error: pre-commit command not found"
```bash
# Instalar pre-commit primero
uv add --dev pre-commit

# Luego instalar hooks
uv run pre-commit install
```

#### "Quiero saltarme los hooks temporalmente"
```bash
# Solo para esta vez (NO recomendado)
git commit -m "mensaje" --no-verify
```

#### "¿Cómo desinstalar pre-commit?"
```bash
# Remover hooks de git
uv run pre-commit uninstall

# O manualmente
rm .git/hooks/pre-commit
```

---

## 7. Common uv usage

Run a script:

```bash
uv run main.py
```

Sync dependencies (e.g., after cloning the repo):

```bash
uv sync
```

Install and use a specific Python version:

```bash
uv python install 3.12
```

---

**💡 Tip:** There's a "UV Toolkit" extension in the VSCode Marketplace to integrate **uv** commands into the editor.
