# Dev and prod have diff ports
5000 vs 1337

# DEV... Build, run and check logs
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

# After gunicorn & .env.prod & .env.prod.db added, run production
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml logs -f

# Make a new entrypoint.prod and chmod it
chmod +x services/web/entrypoint.prod.sh

# Will need a new Dockerfile (Dockerfile.prod)
View Dockerfile.prod for notes

# Tear down old prod and rebuild and run (need to create a db this time)
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db

# See .env.prod.db file for connection string
docker-compose exec db psql --username=hello_flask --dbname=hello_flask_prod


# Add nginx files, Expose port interanlly in docker-compose.prod.yml
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml logs -f

Perhaps the web/project folder will contain final app?

# Static (dev)
add static folder to web/project
Add route handler to __init__.py
import send_from_file to __init__.py
add STATIC_FOLDER to Config class
APP_FOLDER=/usr/src/app to .env.dev

# Static prod
To web and nginx services in docker-compose.prod.yml
    volumes:
        - static_volume:/home/app/web/project/static
volumes:
  postgres_data:
  static_volume:

To nginx.conf
location /static/ {
        alias /home/app/web/project/static/;
    }
APP_FOLDER=/home/app/web to .env.prod

# rebuild and up
http://localhost:1337/static/hello.txt

docker-compose down -v --remove-orphans


docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
docker-compose -f docker-compose.prod.yml logs -f

visit http://localhost:1337/static/hello.txt and view logs