#!/bin/bash

# Prepare log files and start out putting log files to stdout
#touch /srv/logs/gunicorn.log
#touch /srv/logs/access.log
#tail -n 0 -f /srv/logs/*.log &
#

######################################################
# How to fetch credentials?
# you can get credentials from google cloud console
# or alternative using the following command:
# gcloud container clusters get-credentials NAME [--zone ZONE, -z ZONE] [GLOBAL-FLAG …]
# Eg: gcloud container clusters get-credentials testing_cluster
# for more details check - https://goo.gl/I6ci6K
######################################################
export GOOGLE_APPLICATION_CREDENTIALS=/credentials.json
/cloud_sql_proxy -dir=/cloudsql -instances=<CLOUD_SQL_INSTANCE_CONNECTION_NAME>=tcp:3306 &
nginx &

# Wait for above cloud sql proxy to initialize,
# We tried without waiting and it fails sometime to connect so to be on safeside
sleep 5s

python manage.py migrate                  # Apply database migrations
python manage.py collectstatic --noinput  # Collect static files


# Start Gunicorn processes
echo Strating Gunicorn
exec gunicorn TestApp.wsgi:application \
  --name <APP_NAME> \
  --bind 127.0.0.1:8080 \
  --workers 3 \
  --log-level=info \
  "$@"