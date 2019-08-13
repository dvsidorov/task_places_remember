#!/usr/bin/env bash


SRC=$PWD/places_remember/
PYTHONPATH=$SRC
cd $SRC


PYTHONPATH=$PYTHONPATH python manage.py $1
