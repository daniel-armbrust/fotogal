#!/bin/sh
#
# scripts/start_dev.sh
#

export FLASK_APP=fotogal.py
export FLASK_DEBUG=1
export FLASK_ENV=development
export STATIC_URL=/static

cd ../fotogal

flask run --host 0.0.0.0

exit 0
