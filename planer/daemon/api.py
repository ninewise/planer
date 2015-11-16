
import flask

from pony.orm import db_session

from planer.daemon.db import db
from planer.daemon.json_converter import to_json

app = flask.Flask("Planer Http API")


@app.route('/calendars', methods=["GET"])
@db_session
def calendars():
    return to_json(db.Calendar.select())


@app.route('/calendars/<int:calendar>', methods=["GET"])
@db_session
def get_calendar(calendar):
    return to_json(db.Calendar[calendar])


@app.route('/events', methods=["GET"])
@db_session
def events():
    return to_json(db.Event.select())


@app.route('/events/<int:event>', methods=["GET"])
@db_session
def get_event(event):
    return to_json(db.Event[event])


@app.route('/events/new', methods=["POST"])
def new_event():
    pass


