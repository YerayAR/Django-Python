"""Punto de entrada ASGI para servidores asíncronos."""

import os
from django.core.asgi import get_asgi_application

# Configura el módulo de ajustes de Django antes de crear la aplicación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
