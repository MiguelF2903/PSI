#!/bin/bash

# Detener el script si algún test falla
set -e

echo "=========================================="
echo " 🕵️  INICIANDO TESTS Y COBERTURA"
echo "=========================================="

# 1. Borrar datos de cobertura anteriores [cite: 118]
echo "--> Limpiando datos antiguos de coverage..."
python3 -m coverage erase

# 2. Ejecutar TODOS los tests bajo vigilancia de coverage
# Se usa --omit para ignorar los archivos de test y --source=catalog para medir solo la app
# Se añade --verbosity 2 como pide el enunciado para ver detalles [cite: 119, 225]
echo "--> Ejecutando tests (Semana 1, 2, etc)..."
python3 -m coverage run --omit="*/test*" --source=catalog manage.py test catalog.tests --verbosity 2

# 3. Mostrar el reporte en pantalla [cite: 119]
echo "=========================================="
echo " 📊 REPORTE DE COBERTURA"
echo "=========================================="
python3 -m coverage report -m -i

# 4. Guardar el reporte en coverage.txt (Obligatorio para la entrega) 
echo "--> Guardando resultado en 'coverage.txt'..."
python3 -m coverage report -m -i > coverage.txt

echo "=========================================="
echo " ¡PROCESO COMPLETADO! ✅"
echo " Tienes el fichero coverage.txt listo."
echo "=========================================="