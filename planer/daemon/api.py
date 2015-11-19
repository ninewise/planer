
from flask import Flask, request
from werkzeug.exceptions import HTTPException, default_exceptions
from pony.orm import db_session, select
from simpledate import SimpleDate

from planer.daemon.db import db
from planer.daemon.json_converter import as_json
from planer.config import config

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


@app.route('/calendars/<int:calendar>/events', methods=["GET"])
@db_session
def get_calendar_events(calendar):
    return as_json(select(e.id for e in db.Event if e.calendar ==
        db.Calendar[calendar]))
    #return as_json([e.id for e in db.Calendar[calendar].events])


@app.route('/events/<int:event>', methods=["GET"])
@db_session
def get_event(event):
    return as_json(db.Event[event])


@app.route('/events/new', methods=["POST"])
@db_session
def new_event():
    event = dict(calendar=db.Calendar[request.form['calendar']],
                 summary=request.form['summary'],
                 description=request.form.get('description', None),
                 location=request.form.get('location', ''))
    timezone = request.form.get('timezone', config['remote']['timezone'])
    event['start_time'] = SimpleDate(
            request.form['start_time'],
            tz=timezone).datetime
    event['end_time'] = SimpleDate(
            request.form['end_time'],
            tz=timezone).datetime
    db.Event(**event)
    return as_json(dict(message="OK"))


@app.route('/events/interval', methods=["GET"])
def event_interval():
    pass


# Handling error's (source: http://flask.pocoo.org/snippets/83/)
def make_json_error(ex):
    response = as_json(
            { "message": str(ex) },
            status=ex.code if isinstance(ex, HTTPException) else 500)
    return response

for code in default_exceptions:
    app.errorhandler(code)(make_json_error)

