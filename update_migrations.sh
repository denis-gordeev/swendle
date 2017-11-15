SETTINGS_MODE=prod python3 manage.py makemigrations
SETTINGS_MODE=prod python3 manage.py migrate
SETTINGS_MODE=prod python3 manage.py collectstatic
