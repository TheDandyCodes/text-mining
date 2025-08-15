#!/bin/bash
# Script para ejecutar herramientas de calidad de código manualmente

echo "🔧 Ejecutando herramientas de calidad de código con Ruff..."

echo "1. Ejecutando linter de Ruff (incluye correcciones automáticas)..."
uv run ruff check --fix *.py Task_2/*.py

echo "2. Formateando código con Ruff (reemplaza Black e isort)..."
uv run ruff format *.py Task_2/*.py

echo "3. Ejecutando todos los hooks de pre-commit..."
uv run pre-commit run --all-files

echo "✅ ¡Listo! Tu código está limpio y formateado con Ruff."
