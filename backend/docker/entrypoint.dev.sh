#!/bin/sh

cd domuwa
fastapi dev main.py --host 0.0.0.0 --port 8000

exec "$@"
