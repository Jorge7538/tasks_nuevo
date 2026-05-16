# Task List Django Project

Proyecto de ejemplo para gestionar una lista de tareas usando Django.

Este README incluye instrucciones completas para instalar, ejecutar, desarrollar y desplegar localmente el proyecto en Windows (PowerShell). También contiene soluciones a errores comunes que puedes encontrar (por ejemplo plantillas faltantes o problemas con `.git/config`).

## Contenido
- Descripción
- Requisitos
- Preparación del entorno (PowerShell)
- Ejecutar la aplicación
- Estructura del proyecto
- Desarrollo (tests, creación de superusuario)
- Problemas comunes y soluciones
- Contribuir
- Licencia

## Descripción
Esta pequeña aplicación Django maneja una lista de tareas (CRUD parcial). Contiene una app `tasks` que define el modelo `Task`, vistas basadas en clases para listar y ver detalles, plantillas en la carpeta `templates/` y recursos estáticos en `static/`.

## Requisitos
- Python 3.11 (el proyecto usa 3.11 en el entorno virtual actual)
- pip
- Git (opcional pero recomendado)

El proyecto ya incluye un archivo `requirements.txt` con las dependencias necesarias.

## Preparación del entorno (PowerShell)
Abre PowerShell en la carpeta raíz del proyecto (`C:\Users\Jorge Canelon\Pictures\task_list26`) y ejecuta:

```powershell
# Crear y activar un entorno virtual (si no existe)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Actualizar pip y luego instalar dependencias
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si tu política de ejecución de PowerShell no permite ejecutar scripts, puedes habilitar temporalmente la ejecución con (ejecutar como administrador si es necesario):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Migraciones y datos iniciales
```powershell
# Crear migraciones (si hiciste cambios) y aplicarlas
python manage.py makemigrations
python manage.py migrate

# (Opcional) crear un superusuario para acceder al admin
python manage.py createsuperuser
```

## Ejecutar el servidor de desarrollo
```powershell
python manage.py runserver
# Luego abre http://127.0.0.1:8000/ (o la URL que use tu proyecto)
```

## Archivos importantes y estructura

Raíz del proyecto (los más relevantes):

- `manage.py` — script de entrada de Django
- `db.sqlite3` — base de datos SQLite (local)
- `requirements.txt` — dependencias
- `base_project/` — configuración del proyecto (settings, urls, wsgi, asgi)
- `tasks/` — app principal con `models.py`, `views.py`, `urls.py`, `templates/`, etc.
- `templates/` — plantillas HTML globales (por ejemplo `tasks_list.html`, `task-detail.html`, `_base.html`)
- `static/` — CSS/JS/imagenes (ej. `static/css/style.css`)

En `base_project/settings.py` se configura `TEMPLATES['DIRS'] = [BASE_DIR / 'templates']` y `APP_DIRS = True`, por tanto Django busca plantillas tanto en `templates/` global como en `templates/` dentro de cada app.

## Plantillas
- `templates/tasks_list.html` — lista de tareas
- `templates/task-detail.html` — detalle de una tarea
- `templates/_base.html` — layout base

Si al abrir una URL obtienes `TemplateDoesNotExist`, revisa:

1. Que exista el archivo con el nombre correcto (por ejemplo `task-detail.html`).
2. Que la ruta `TEMPLATES['DIRS']` en `base_project/settings.py` incluya la carpeta `templates` (por defecto está configurada).
3. Que la vista pase el contexto esperado (puedes forzar `context_object_name = 'task'` en tu `DetailView`).

Ejemplo (en `tasks/views.py`) para asegurar que la plantilla reciba `task`:

```python
from django.views.generic import DetailView
from .models import Task

class TaskDetailView(DetailView):
    model = Task
    template_name = 'task-detail.html'
    context_object_name = 'task'
```

## Archivos estáticos
Durante desarrollo, Django sirve archivos estáticos automáticamente cuando `DEBUG = True`. Si quieres recolectarlos para producción:

```powershell
python manage.py collectstatic --noinput
```

Configura `STATIC_ROOT` en `settings.py` cuando prepares despliegue en producción.

## Git y remotos (nota sobre `.git/config` corrupto)

Si al usar git obtienes errores como `fatal: bad config line 1 in file .../.git/config`, es posible que el archivo `config` dentro de `.git/` esté corrupto. Durante el desarrollo se creó automáticamente un respaldo llamado `.git/config.bad` y se reemplazó por un `config` mínimo. Si necesitas restaurar remotos o la URL `origin`, sigue estos pasos:

1. Buscar URL en el archivo de respaldo (si existe):

```powershell
git config -f .git/config.bad --get remote.origin.url
```

2. Si obtienes la URL, re-agrega el remoto:

```powershell
git remote add origin <la-url-recuperada>
git push -u origin main
```

3. Para comprobar remotos actuales:

```powershell
git remote -v
```

Si no tienes el `.git/config.bad` o no contiene la URL, puedes volver a crear el repositorio en GitHub/GitLab/Azure e indicar la URL remota con `git remote add origin <url>`.

## Tests
Si incluyes tests en `tasks/tests.py`, ejecútalos con:

```powershell
python manage.py test
```

## Solución de problemas comunes

- TemplateDoesNotExist: asegúrate de que el archivo `.html` exista y que `TEMPLATES` incluya la ruta correcta.
- `fatal: 'origin' does not appear to be a git repository`: agrega el remoto con `git remote add origin <url>` y luego `git push -u origin main`.
- Errores de permisos en PowerShell al activar el entorno: usar `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`.

## Contribuir
Si quieres contribuir:

1. Haz un fork o crea una rama nueva.
2. Crear una rama feature/bugfix.
3. Haz tus cambios, añade tests si aplica.
4. `git commit -m "Descripción corta"` y `git push`.
5. Abre un Pull Request describiendo los cambios.

## Despliegue
Para producción:

- Usa una base de datos más robusta (Postgres o similar).
- Configura `DEBUG = False` y `ALLOWED_HOSTS` en `settings.py`.
- Sirve archivos estáticos desde un CDN o servidor (configurar `STATIC_ROOT` y `collectstatic`).
- Usa un servidor WSGI (Gunicorn, uWSGI) y un servidor web/proxy (Nginx, IIS) según tu infraestructura.

## Autor
Jorge Canelon

---
Si quieres, puedo añadir un ejemplo de `docker-compose.yml` para ejecutar la app en contenedores, o crear un archivo `requirements-dev.txt` y pruebas adicionales. Dime qué prefieres.
