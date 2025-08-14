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

## 5. Common uv usage

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
