Planer
======

A flat calendar application.

Features
--------

None

Planned
-------

 * Client-daemon structure.
 * Many accounts, many calendars.
 * Local storage of calendars
 * Integration with Google Calendar. I'll be doing this with the [Google Calendar API](https://developers.google.com/google-apps/calendar/).
 * Imports from and exports to [iCalendar](https://pypi.python.org/pypi/icalendar/) if I feel like it.
 * Curses visualisation of the calendars.
 * Stuff

Notes to self
-------------

 * The main querying interface should be ask for all events (single
   and recurring) within a range. Apart from a whole variety of ways
   to specify ranges, this requires a fast way of looking up events
   in a range.

   For single events, this can be done in a sorted map, with sorting
   on date and entries for both start and end times of the events. For
   recurring events,

   For recurring events, the range of occurence should be checked for
   overlap with the given range. Then, this selection of recurring
   events should be expanded (though only as much as required) and
   checked in the same way as before. Or easier as there should be
   less.
