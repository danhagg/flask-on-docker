import os

from werkzeug.utils import secure_filename

from flask import Flask, jsonify, send_from_directory, request, redirect, url_for
from project.models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object("project.config.Config")

    # Initialize extensions
    db.init_app(app)

    from project.assignment_form.routes import assignment_form

    app.register_blueprint(assignment_form, url_prefix="/assignment_form")

    return app
