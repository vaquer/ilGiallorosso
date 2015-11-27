"""
WSGI config for ilGiallorosso project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import json

from django.core.wsgi import get_wsgi_application

DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__FILE__)))

with open(os.path.join(DIR_BASE, '../conf.json')) as config_file:
    confs = json.loads(config_file.read())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ilGiallorosso.settings")
os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB", confs['general']['db']['name'])
os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_USER_NAME", confs['general']['db']['username'])
os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_PASSWORD", confs['general']['db']['password'])
os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_HOST", confs['general']['db']['host'])
os.environ.setdefault("DJANGO_ILGIALLOROSSO_SECRET_KEY", confs['general']['secretkey'])

application = get_wsgi_application()
