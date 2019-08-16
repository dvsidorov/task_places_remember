release: PYTHONPATH=$PYTHONPATH:/app/places_remember/
release: python places_remember/manage.py makemigrations layer_model && python places_remember/manage.py migrate
web: gunicorn places_remember.config.wsgi --log-file -