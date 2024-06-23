"""
WSGI config for paintsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'paintsite.settings')

application = get_wsgi_application()

application = WhiteNoise(application)
staticfiles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'staticfiles')

# Check if the directory exists before adding files to WhiteNoise
if os.path.isdir(staticfiles_path):
    application.add_files(staticfiles_path, prefix='staticfiles/')