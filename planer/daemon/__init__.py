
from datetime import datetime, timedelta

from pony.orm import db_session

from planer.config import config

from planer.daemon.api import app
from planer.daemon.db import db

with db_session:
    for c in db.Calendar.select():
        c.delete()
    c = db.Calendar(name="Test Calendar")
    db.Event(summary="Test Event 1", start_time=datetime.now(), end_time=datetime.now() + timedelta(hours=1), calendar=c)
    db.Event(summary="Test Event 2", start_time=datetime.now(), end_time=datetime.now() + timedelta(hours=1), calendar=c)

def main():
    app.debug = True
    app.run(host=config['daemon']['host'],
            threaded=True,
            port=int(config['daemon']['port']))

