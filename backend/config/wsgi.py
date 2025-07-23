"""Punto de entrada WSGI para el proyecto Memory Game."""

import os
from django.core.wsgi import get_wsgi_application

# Se define el módulo de ajustes antes de iniciar la aplicación WSGI
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
