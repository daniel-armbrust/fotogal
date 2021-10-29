#!/bin/sh
exec gunicorn --access-logfile - --error-logfile - -w 2 --threads 2 -b 0.0.0.0:5000 fotogal:app