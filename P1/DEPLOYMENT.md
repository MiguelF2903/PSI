# Guía de Despliegue en Render - Práctica 1 PSI

## 📋 Checklist Pre-Despliegue

- [x] Todos los tests pasan (80/80)
- [x] Cobertura de código al 100%
- [x] `requirements.txt` actualizado
- [x] `authors.txt` creado
- [x] `build.sh` creado y con permisos de ejecución
- [x] `.gitignore` configurado correctamente
- [x] Variables de entorno configuradas en `settings.py`

## 🚀 Pasos para Desplegar en Render

### 1. Preparar Base de Datos en Neon.tech

1. Crear cuenta en [Neon.tech](https://neon.tech)
2. Crear un nuevo proyecto PostgreSQL
3. Copiar la `DATABASE_URL` que proporciona Neon
4. Guardar las credenciales:
   - Usuario: `alumnodb`
   - Contraseña: `alumnodb`

### 2. Subir Código a GitHub

```bash
git add .
git commit -m "Preparado para deployment en Render"
git push origin main
```

### 3. Configurar Render

1. Crear cuenta en [Render.com](https://render.com)
2. Crear un **New Web Service**
3. Conectar con tu repositorio de GitHub
4. Configurar el servicio:
   - **Name**: `P1_[EQUIPO]_2311_2026_1` (ejemplo: `P1_10_2311_2026_1`)
   - **Region**: Frankfurt (EU Central)
   - **Branch**: main
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn locallibrary.wsgi:application`
   - **Instance Type**: Free

### 4. Configurar Variables de Entorno en Render

En la sección "Environment" de Render, agregar:

```
DJANGO_SECRET_KEY=<generar-una-clave-secreta-nueva>
DJANGO_DEBUG=False
DATABASE_URL=<tu-database-url-de-neon>
ALLOWED_HOSTS=.onrender.com,localhost,127.0.0.1
PYTHON_VERSION=3.12.0
```

**Importante**: Para generar una nueva SECRET_KEY segura:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Poblar la Base de Datos

Una vez desplegado, conectarse a la base de datos y ejecutar:

```bash
# Desde el shell de Render o localmente con DATABASE_URL de Neon
python manage.py migrate
python manage.py createsuperuser --username alumnodb --email alumnodb@example.com
# Contraseña: alumnodb

# Poblar con datos de ejemplo
python populate_catalog.py
```

### 6. Verificar el Despliegue

1. Acceder a: `https://P1_[EQUIPO]_2311_2026_1.onrender.com/`
2. Verificar que la aplicación carga correctamente
3. Acceder al admin: `https://P1_[EQUIPO]_2311_2026_1.onrender.com/admin/`
4. Login con `alumnodb` / `alumnodb`

## 📝 URL Final

La URL debe tener el formato:
```
https://P1_[EQUIPO]_2311_2026_1.onrender.com/
```

Donde:
- `P1` = Práctica 1
- `[EQUIPO]` = Número de equipo/pareja
- `2311` = Grupo
- `2026` = Año
- `1` = Versión

## 🔧 Configuración Local vs Producción

### Local (Desarrollo)
- `DEBUG=True` (por defecto)
- Base de datos PostgreSQL local
- Archivos estáticos servidos por Django

### Producción (Render)
- `DEBUG=False` (configurado en variables de entorno)
- Base de datos PostgreSQL en Neon.tech
- Archivos estáticos servidos por WhiteNoise
- Gunicorn como servidor WSGI

## 📦 Archivos Importantes

- `build.sh`: Script de construcción para Render
- `requirements.txt`: Dependencias de Python
- `authors.txt`: Información del equipo
- `coverage.txt`: Reporte de cobertura de tests
- `.env.example`: Plantilla de variables de entorno
- `.gitignore`: Archivos a ignorar en Git

## ⚠️ Notas Importantes

1. **NO** subir el archivo `.env` a GitHub (contiene secretos)
2. La primera carga en Render puede tardar varios minutos
3. Render puede dormir el servicio gratuito después de inactividad
4. Verificar que `ALLOWED_HOSTS` incluye el dominio de Render
5. Asegurarse de que la base de datos en Neon esté poblada

## 🐛 Troubleshooting

### Error: "DisallowedHost"
- Verificar que `ALLOWED_HOSTS` incluye `.onrender.com`

### Error: "Static files not found"
- Ejecutar `python manage.py collectstatic` en el build

### Error de Base de Datos
- Verificar que `DATABASE_URL` está correctamente configurada
- Verificar que las migraciones se ejecutaron

### Tests fallan en producción
- Asegurarse de que `DEBUG=False` en producción
- Verificar que todos los archivos estáticos están recolectados
