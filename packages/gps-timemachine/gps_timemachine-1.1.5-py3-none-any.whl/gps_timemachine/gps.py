import datetime as dt
import logging
from importlib import resources
from urllib.request import urlopen
from urllib.error import URLError, HTTPError, ContentTooShortError
import socket
from functools import lru_cache

from . import static

# UNCOMMENT THIS WHEN WE DO ERROR REPORTING AGAIN
# from .errors import LeapSecondsDataUnavailable

"""
NOTES on GPS -> UTC convertion
------------------------------

GPS time is offset from UTC because UTC time includes leap seconds but GPS does
not. Unfortunately, leap seconds are not added on a well defined schedule, so
the only way to know the GPS-UTC offset is to look up the historical record of
leap second additions. We currently know of three ways this can be accomplished:

1) CURRENTLY IMPLEMENTED - Query a remote resource to get the current list of
leap seconds. In this case, we're using a url at the US Naval Observatory, but
there may be others. With the list of leap seconds and when they were applied,
you can determine the appropriate GPS-UTC offset for any date.
PROS - should always be up-to-date. Fast.
CONS - relies on an external url which could be down for some reason

2) Python package - Use a python package like astropy that has different time
conversions built in. For a possible implementation, see
https://bitbucket.org/nsidc/valkyrie-ingest/commits/51631bdfe3a5ea875f430bd55b60fe18f98174aa.
which uses TAI time as an intermediate. TAI is always 19 seconds ahead of GPS,
and GPS is a variable number of seconds ahead of UTC, depending on the date and t
ime. For exact delta between UTC and TAI, see:
http://hpiers.obspm.fr/eop-pc/index.php?index=TAI-UTC_tab&lang=en
PROS - no external resources required
CONS - First implementation was much slower. Package may need to be updated to
get new leap seconds as they are added?

3) OS file - Read the file(s) on the OS that store time and date information.
For example, /usr/share/zoneinfo
PROS - should be fast, like option #1. Doesn't rely on an external url
CONS - could be platform dependent? OS would need to be updated to get new
files as they are available.
"""


def _get_tai_utc():
    # Add URLS as needed. We have encountered errors with various servers over
    # the years, and now there is only one known source of the data that's
    # publicly available and not behind earthdata login. A mirror of the navy
    # tai-utc.dat file can be found here:
    # https://cddis.nasa.gov/archive/products/iers/tai-utc.dat, behind earthdata
    # login. Earthdata login is not currently supported by gps-timemachine.
    URLS_TO_TRY = ('https://maia.usno.navy.mil/ser7/tai-utc.dat',)

    for url in URLS_TO_TRY:
        try:
            f = urlopen(url, timeout=5)
            return f
        except (URLError, HTTPError, ContentTooShortError,
                TimeoutError, socket.error):
            pass

    f = resources.open_text(static, 'tai-utc.dat')
    logging.warning('Attempts to retrieve tia-utc.dat file remotely failed, using local copy instead...')
    return f


def load_leap_seconds():
    """Loads the historical record of leap seconds from the Time Service Dept.
    of the US Naval Observatory

    Parameters
    ----------
    N/A

    Returns
    -------
    leap_seconds
        A list of tuples containing the python datetime and total number of
        leap seconds for each leap second addition
        Example:
        [(datetime1, 25.0), (datetime2, 26.0)]

    """
    f = _get_tai_utc()

    leap_seconds = []
    for line in f:
        if not isinstance(line, str):
            line = line.decode('utf-8')
        data = line.split()
        day = data[2] if len(data[2]) == 2 else '0' + data[2]
        date_str = data[0] + data[1] + day
        date = dt.datetime.strptime(date_str, '%Y%b%d')
        # gps was sychronized with utc on 1980-01-06 at which point there were
        # already 19 leap seconds
        leap_seconds.append((date, float(data[6]) - 19))

    return leap_seconds


@lru_cache()
def get_leap_seconds():

    return load_leap_seconds()


def _gps_time_parts(gps_time):
    h = int(gps_time / 1e4)
    m = int((gps_time % 1e4) / 100)
    s = int(gps_time % 100)
    ms = int(round((gps_time % 1) * 1000))

    if ms == 1000:
        s += 1
        ms = 0

    return (h, m, s, ms)


def leap_seconds(dt):
    """
    search the historical leap second record to find in the correct number of
    leap seconds to apply to the given datetime
    Parameters
    ----------
    dt (type: datetime)
        datetime for which to find the correct number of leap seconds
    
    Returns
    -------
    leap_seconds (type: float)
        number of leap seconds
    """
    idx = len(get_leap_seconds()) - 1
    # start at the end of the list becuase most data falls later in the 1961 - present record
    while get_leap_seconds()[idx][0] > dt:
        idx -= 1
    leap_seconds = get_leap_seconds()[idx][1]
    return leap_seconds


def gps_to_utc(date, gps_time):
    """Convert the GPS time on a given date into a UTC datetime.

    Parameters
    ----------
    date
        The date (datetime.date) on which the gps_time is referenced.
    gps_time
        The GPS time (float) for the given date. E.g., 12:34:56.789
        is the floating point number 123456.789.
    
    Returns
    -------
    datetime
        A datetime (datetime.datetime) in UTC for the given date and gps_time.
    """

    hours, minutes, seconds, milliseconds = _gps_time_parts(gps_time)
    if (seconds > 59):
        msg = 'Invalid gps_time on {0}: {1}.'.format(date, gps_time)
        logging.warning(msg)
        milliseconds = 0
        seconds = 0
        minutes = (minutes + 1) % 60
        if minutes == 0:
            hours = (hours + 1) % 24
        if hours == 0:
            date = date + dt.timedelta(days=1)
        msg = 'Corrected to {0} {1}:{2}:{3}.{4}.'.format(date, hours, minutes,
                                                         seconds, milliseconds)
        logging.warning(msg)
    gps_dt = dt.datetime(date.year, date.month, date.day, hour=hours,
                         minute=minutes, second=seconds, microsecond=milliseconds*1000)
    utc_dt = gps_dt - dt.timedelta(seconds=leap_seconds(gps_dt))

    return utc_dt
