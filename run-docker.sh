pipenv shell
pipenv install
python manage.py makemigrations
python manage.py makemigrations trashusers
python manage.py makemigrations trashimages
python manage.py makemigrations trashmonsters
python manage.py makemigrations trashmain
python manage.py makemigrations trashsite
docker-compose run web python src/manage.py migrate
docker-compose build
docker-compose up -d
