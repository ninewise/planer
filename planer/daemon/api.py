
from flask import Flask
from werkzeug.exceptions import HTTPException, default_exceptions
from pony.orm import db_session

from planer.daemon.db import db
from planer.daemon.json_converter import as_json

__all__ = ["app"]

app = Flask("Planer Http API")


@app.route('/calendars', methods=["GET"])
@db_session
def calendars():
    return as_json(db.Calendar.select())


@app.route('/calendars/<int:calendar>', methods=["GET"])
@db_session
def get_calendar(calendar):
    return as_json(db.Calendar[calendar])


@app.route('/events/<int:event>', methods=["GET"])
@db_session
def get_event(event):
    return as_json(db.Event[event])


@app.route('/events/new', methods=["POST"])
def new_event():
    pass


# Handling error's (source: http://flask.pocoo.org/snippets/83/)
def make_json_error(ex):
    response = as_json(
            { "message": str(ex) },
            status=ex.code if isinstance(ex, HTTPException) else 500)
    return response

for code in default_exceptions:
    app.errorhandler(code)(make_json_error)

