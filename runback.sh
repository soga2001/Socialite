source venv/bin/activate
cd backend
# python3 manage.py runserver
# daphne -b 0.0.0.0 -p 8000 config.asgi:application  -v2
# python manage.py runserver -v2
python3 manage.py runserver_plus --cert-file /Users/Suyogya/Projects/BasedBook/localhost.pem --key-file /Users/Suyogya/Projects/BasedBook/localhost-key.pem
# gunicorn -b localhost:8000 backend.wsgi:application --reload