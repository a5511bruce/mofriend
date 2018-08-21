release: python manage.py migrate
web: gunicorn mofriend.wsgi --log-file -
web: bundle exec rails server -p $PORT
