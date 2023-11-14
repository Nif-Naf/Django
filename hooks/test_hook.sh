#!/bin/bash

if docker ps --format '{{.Names}} {{.Status}}' | grep -qi "django up"
then
  echo "Run testing in running container: 'django'."
  command docker-compose exec -T django python manage.py test
else
  echo "Run testing local."
  command python manage.py test
fi
