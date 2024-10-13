python -m venv ./.venv
pipenv install

python manage.py migrate
python manage.py runserver