
import flask

from pony.orm import db_session

from planer.daemon.db import db
from planer.daemon.json_converter import as_json

app = flask.Flask("Planer Http API")


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


