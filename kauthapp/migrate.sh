#!/bin/sh

python3 -m manage makemigrations
python3 -m manage migrate
