"""

This modeule configures the Flask CLI tool to...
run and manage the app from the command line

"""

from flask.cli import FlaskGroup

from project import app, db, User

# created a new FlaskGroup instance
# Extends the normal CLI with commands related to Flask app
cli = FlaskGroup(app)


# docker-compose exec web python manage.py create_db
@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


# docker-compose exec web python manage.py seed_db
@cli.command("seed_db")
def seed_db():
    db.session.add(User(email="danielhaggerty1976@gmail.com"))
    db.session.commit()


if __name__ == "__main__":
    cli()
