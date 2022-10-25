#!/bin/sh

gunicorn --workers 3 --bind 0.0.0.0:8080 --log-level debug --proxy-allow-from "*" --forwarded-allow-ips "*" core.wsgi
