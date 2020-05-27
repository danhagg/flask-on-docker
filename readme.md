# Build, run and check logs
docker-compose build
docker-compose up -d

docker-compose logs -f

# Tear down to rebuild (see first command)
docker-compose down -v

# Create table in postgres via create_db cli
docker-compose exec web python manage.py create_db

# check table created by logging into postgres container
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
# list dbs, connect to db, list tables
\l
\c hello_flask_dev
\dt

# Check volume created
docker volume inspect flask-on-docker_postgres_data

# Do user seeding then check
docker-compose exec web python manage.py seed_db
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_dev
\c hello_flask_dev
select * from users;

# Can build without posgres
docker build -f ./services/web/Dockerfile -t hello_flask:latest ./services/web
# then run (check localhost:5001)
docker run -p 5001:5000 \
    -e "FLASK_APP=project/__init__.py" -e "FLASK_ENV=development" \
    hello_flask python /usr/src/app/manage.py run -h 0.0.0.0