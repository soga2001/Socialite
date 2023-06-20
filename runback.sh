source venv/bin/activate
cd backend
# python3 manage.py runserver
# python3 run_daphne.py runserver
# daphne -b 0.0.0.0 -p 8000 backend.asgi:application  -v2
# export DJANGO_MODULE=backend.settings
daphne -e ssl:8000:privateKey=/Users/Suyogya/Projects/BasedBook/localhost-key.pem:certKey=/Users/Suyogya/Projects/BasedBook/localhost.pem backend.asgi:application
# python manage.py runserver -v2
# python3 manage.py runserver_plus --cert-file /Users/Suyogya/Projects/BasedBook/localhost.pem --key-file /Users/Suyogya/Projects/BasedBook/localhost-key.pem
# gunicorn -b localhost:8000 backend.wsgi:application --reload


# daphne -e ssl:8000:privateKey=/Users/Suyogya/Projects/BasedBook/selfsigned.key:certKey=/Users/Suyogya/Projects/BasedBook/selfsigned.crt backend.asgi:application
