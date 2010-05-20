"""
Drop-in replacement for Python's datetime module.

Importing the datetime module
-----------------------------

Here are some examples using the datetime module:

    # If you're just importing the standard module:
    >>> import datetime

    # If you want to use the timemachine module:
    >>> from timemachine import machine as datetime

    # Then, your code can remain the same:
    >>> print datetime.datetime.utcnow()

Importing the datetime class
----------------------------

Sadly, we must continue the bad naming practice for the 'datetime' class;
it really should have been named 'DateTime', but it wasn't. Oh well.

Here's how you can import the 'datetime' class.

    # If you just want to import the standard 'datetime' class:
    >>> from datetime import datetime

    # If you want to use the timemachine's 'datetime' class:
    >>> from timemachine.machine import datetime

    # Then, your code can remain the same:
    >>> print datetime.utcnow()

Using the timemachine 'pass-thru' mode:
---------------------------------------

Pass-thru mode makes the timemachine work exactly like the standard module.

    >>> from timemachine import machine as datetime
    >>> datetime.set_passthru_mode() # this is actually the default mode
    >>> print datetime.datetime.utcnow()

    (It will print the current date in UTC.)

Using the timemachine 'fixed' mode:
-----------------------------------

Fixed mode makes the timemachine stay on a pre-set datetime.

    >>> from timemachine import machine as datetime
    >>> datetime.set_fixed_mode(2010, 12, 25, 23, 59, 59) # 1 sec. to Santa! :)
    >>> print datetime.datetime.utcnow()
    datetime.datetime(2010, 12, 25, 23, 59, 59, ...)

Using the timemachine 'offset' mode:
------------------------------------

In offset mode, the timemachine reports time that has been offset from the current time.

    >>> from timemachine import machine as datetime
    >>> datetime.set_offset_mode(years=-1) # Last year.
    # Assuming that utcnow() returns 1 sec. to Santa in 2010...
    >>> print datetime.datetime.utcnow()
    datetime.datetime(2009, 12, 25, 23, 59, 59, ...)

"""
import datetime as _datetime #python's standard datetime module

__all__ = [
    # All the attributes of the standard datetime module:
    'MAXYEAR', 'MINYEAR',
    '__doc__', '__file__', '__name__', '__package__',
    'date', 'datetime', 'datetime_CAPI', 'time', 'timedelta', 'tzinfo',
    # Plus some special ones for timemachine:
    'in_fixed_mode', 'in_offset_mode', 'in_passthru_mode',
    'increment_fixed_mode',
    'set_fixed_mode', 'set_offset_mode', 'set_passthru_mode',
]

# Attributes we just pass along from the standard datetime module:
MAXYEAR = _datetime.MAXYEAR
MINYEAR = _datetime.MINYEAR
# Not sure what this does, but let's pass it along anyway:
datetime_CAPI = _datetime.datetime_CAPI
timedelta = _datetime.timedelta
tzinfo = _datetime.tzinfo


# Time machine control constants and variables:
PASSTHRU_MODE = 0
FIXED_MODE = 1
OFFSET_MODE = 2
_mode = PASSTHRU_MODE
_fixed_date = None
_fixed_datetime = None
#REVIEW: Do you need to add _offset here, since it is used as a global later?
_offset_delta = None

def in_passthru_mode():
    global _mode
    return (_mode == PASSTHRU_MODE)

def in_fixed_mode():
    global _mode
    return (_mode == FIXED_MODE)

def in_offset_mode():
    global _mode
    return (_mode == OFFSET_MODE)

def set_passthru_mode():
    global _mode
    global _fixed_date
    global _fixed_datetime
    global _offset
    #REVIEW: Do you need to add global _offset_delta?
    _mode = PASSTHRU_MODE
    _fixed_date = None
    _fixed_datetime = None
    _offset = None
    _offset_delta = None

def set_fixed_mode(year, month, day,
                   hour=0, minute=0, second=0,
                   microsecond=0, tzinfo=None):
    global _mode
    global _fixed_date
    global _fixed_datetime
    global _offset
    #REVIEW: Do you need to add global _offset_delta?    
    _mode = FIXED_MODE
    _fixed_date = _datetime.date(year, month, day)
    _fixed_datetime = _datetime.datetime(year, month, day,
                   hour=0, minute=0, second=0,
                   microsecond=0, tzinfo=None)
    _offset = None
    _offset_delta = None

def increment_fixed_mode(days=0, seconds=0, microseconds=0,
                         milliseconds=0, minutes=0, hours=0, weeks=0):
    global _mode
    global _fixed_date
    global _fixed_datetime
    assert (_mode == FIXED_MODE), 'Cannot increment unless in fixed mode!'
    delta = _datetime.timedelta(days, seconds, microseconds,
                                milliseconds, minutes, hours, weeks)
    _fixed_date = _fixed_date + delta
    _fixed_datetime = _fixed_datetime + delta

def set_offset_mode(days=0, seconds=0, microseconds=0,
                    milliseconds=0, minutes=0, hours=0, weeks=0):
    global _mode
    global _fixed_date
    global _fixed_datetime
    #REVIEW: Do you need to replace this with global _offset_delta?  
    global _offset
  
    _mode = OFFSET_MODE
    _fixed_date = None
    _fixed_datetime = None
    _offset_delta = _datetime.timedelta(days, seconds, microseconds,
                                        milliseconds, minutes, hours, weeks)

# Our own classes that override the standard datetime module:
# NOTE: I hope this doesn't mess up the object signatures, if anyone is checking.
class date(_datetime.date):
    def _get_offset_time(self):
        global _offset_delta
        return (self + _offset_delta)

    def ctime(self):
        if in_fixed_mode():
            return _fixed_date.ctime()
        if in_offset_mode():
            return self._get_offset_time().ctime()
        return super(self, date).ctime()

"""
#TODO: Code the rest of these.
    def day(self):

    def isocalendar(self):

    def isoformat(self):

    def isoweekday(self):

    def month(self):

    def replace(self):

    def resolution(self):

    def strftime(self):

    def timetuple(self):

    def today(self):

    def toordinal(self):

    def weekday(self):

    def year(self):
"""



class datetime(_datetime.datetime):
    #TODO: Code similar to date.
    pass

class time(_datetime.time):
    #TODO: Code similar to date.
    pass