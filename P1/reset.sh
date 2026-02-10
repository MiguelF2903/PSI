#!/bin/bash

# Detener el script si ocurre algún error
set -e

echo "=========================================="
echo " INICIANDO RESET DE LA BASE DE DATOS"
echo "=========================================="

# 1. Borrar y Crear Base de Datos PostgreSQL
# Nota: Si es la primera vez y la BD no existe, dropdb fallará.
# El '|| true' hace que el script continue aunque falle el dropdb.
echo "--> Reiniciando PostgreSQL (PSI)..."
dropdb -U alumnodb -h localhost psi || true
createdb -U alumnodb -h localhost psi

# 2. Migraciones
echo "--> Creando y aplicando migraciones..."
python3 manage.py makemigrations
python3 manage.py migrate

# 3. Poblar datos
echo "--> Ejecutando script de población..."
python3 populate_catalog.py

# 4. Crear Superusuario Automáticamente
# Definimos las variables de entorno temporalmente para este comando
echo "--> Creando Superusuario 'alumnodb'..."
export DJANGO_SUPERUSER_PASSWORD=alumnodb
python3 manage.py createsuperuser --username alumnodb --email admin@example.com --noinput

echo "=========================================="
echo " ¡LISTO! PROCESO TERMINADO CON ÉXITO"
echo "=========================================="