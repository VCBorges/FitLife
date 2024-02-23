"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

DJANGO_SETTINGS_MODULE = os.getenv("DJANGO_SETTINGS_MODULE") or 'dev'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'config.settings.{DJANGO_SETTINGS_MODULE}')

application = get_wsgi_application()
