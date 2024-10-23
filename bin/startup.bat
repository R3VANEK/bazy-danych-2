python -m venv ./.venv
pipenv install
pipenv shell
python manage.py migrate
python manage.py runserver