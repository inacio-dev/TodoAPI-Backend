#!/bin/bash

docker compose exec api pip install ipython
docker compose exec api python manage.py shell_plus --ipython --print-sql