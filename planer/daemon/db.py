
from datetime import datetime
from pony.orm import Database, PrimaryKey, Required, Set, Optional, sql_debug

from planer.config import config

db = Database("sqlite", config['daemon']['database file'], create_db=True)

class Calendar(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    events = Set("Event")


class GoogleCalendar(db.Calendar):
    synch_token = Required(str, nullable=True)


class Event(db.Entity):
    id = PrimaryKey(int, auto=True)
    summary = Required(str)
    description = Optional(str, default="")
    start_time = Required(datetime)
    end_time = Required(datetime)
    location = Optional(str)
    calendar = Required(Calendar)


sql_debug(True)
db.generate_mapping(create_tables=True)

