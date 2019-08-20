release: rm places_remember/db.sqlite3 && find places_remember/ -path "*/migrations/*.py" -not -name "__init__.py" -delete && find places_remember/ -path "*/migrations/*.pyc"  -delete
release: export PYTHONPATH=$PYTHONPATH:/app/places_remember/
release: python places_remember/manage.py makemigrations layer_model && python places_remember/manage.py migrate
web: gunicorn places_remember.config.wsgi --log-file -