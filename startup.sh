#!/bin/bash

export PYTHONPATH=~/src:$PYTHONPATH
export DJANGO_SETTINGS_MODULE="Franchise.settings"

django-admin runserver $1
