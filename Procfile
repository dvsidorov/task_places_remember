release: rm places_remember/db.sqlite3 && find places_remember/ -path "*/migrations/*.py" -not -name "__init__.py" -delete && find places_remember/ -path "*/migrations/*.pyc"  -delete
release: export PYTHONPATH=$PYTHONPATH:/app/places_remember/
release: python places_remember/manage.py makemigrations layer_model && python places_remember/manage.py migrate
web: gunicorn -w 4 -b 0.0.0.0:5000 \
      --access-logfile - \
      --error-logfile - \
      --access-logformat "%(h)s %(l)s %(u)s %(t)s pid %(p)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(l)s %(D)s µs" \
      "backend.application:init_app()"