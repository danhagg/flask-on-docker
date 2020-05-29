import os

from flask import (
    current_app,
    render_template,
    Blueprint,
    request,
    jsonify,
    send_from_directory,
)

from werkzeug.utils import secure_filename

assignment_form = Blueprint("assignment_form", __name__, template_folder="templates")


@assignment_form.route("/")
def hello_world():
    return jsonify(hello="from the other side")


@assignment_form.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(current_app.config["STATIC_FOLDER"], filename)


@assignment_form.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(current_app.config["MEDIA_FOLDER"], filename)


@assignment_form.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config["MEDIA_FOLDER"], filename))
    return """
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
