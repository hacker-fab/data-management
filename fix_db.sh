rm db.sqlite3
rm -r data_management/migrations
python3 manage.py makemigrations data_management
python3 manage.py migrate
python3 manage.py runserver