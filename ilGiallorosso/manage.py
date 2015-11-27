#!/usr/bin/env python
import os
import sys
import json

if __name__ == "__main__":
    IR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    with open(os.path.join(DIR_BASE, '../conf.json')) as config_file:
        conf = json.loads(config_file.read())

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ilGiallorosso.settings.dev")
    os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB", conf['general']['db']['name'])
    os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_USER_NAME", conf['general']['db']['username'])
    os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_PASSWORD", conf['general']['db']['password'])
    os.environ.setdefault("DJANGO_ILGIALLOROSSO_DB_HOST", conf['general']['db']['host'])
    os.environ.setdefault("DJANGO_ILGIALLOROSSO_SECRET_KEY", conf['general']['secretkey'])

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
