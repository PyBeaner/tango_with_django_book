__author__ = 'PyBeaner'

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tango_with_django.settings")

import django

django.setup()

from rango.models import Category, Page


if __name__ == '__main__':
    pass