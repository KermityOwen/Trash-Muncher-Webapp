docker-compose run web python src/manage.py migrate
docker-compose build
docker-compose up -d