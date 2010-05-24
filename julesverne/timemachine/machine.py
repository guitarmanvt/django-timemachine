"""
Drop-in replacement for Python's standard 'datetime' module.

Importing the datetime module
-----------------------------

Here are some examples using the datetime module:

    # If you're just importing the standard module:
    >>> import datetime

    # If you want to use the timemachine module:
    #REVIEW: Shouldn't this be from machine import datetime?
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

Using the timemachine 'present' mode:
---------------------------------------

Present mode makes the timemachine work exactly like the standard module.

    >>> from timemachine import machine as datetime
    >>> datetime.return_to_present() # this is actually the default mode
    >>> print datetime.datetime.utcnow()

    (It will print the current date in UTC.)

Using the timemachine 'frozen' mode:
-----------------------------------

Frozen mode makes the timemachine stay on a pre-set datetime.

    >>> from timemachine import machine as datetime
    >>> christmas = datetime.datetime(2010, 12, 24, 23, 59, 59) # almost! :)
    >>> datetime.start_freeze_at_datetime(christmas)
    >>> print datetime.datetime.utcnow()
#REVIEW: Shouldn't this be datetime.datetime(2010, 12, 24, 23, 59, 59, ...)
    datetime.datetime(2010, 12, 25, 23, 59, 59, ...)
    >>> sleep(30) #30 seconds
    >>> print datetime.datetime.utcnow() # nothing changes...
#REVIEW: Shouldn't this be datetime.datetime(2010, 12, 24, 23, 59, 59, ...)
    datetime.datetime(2010, 12, 25, 23, 59, 59, ...)
    >>> datetime.move_freeze_by_delta(timedelta(days=7)) # ...until you tell it
    >>> print datetime.datetime.utcnow() # now it reports New Year's Eve! :)
    datetime.datetime(2010, 12, 31, 23, 59, 59, ...)


Using the timemachine 'shifted' mode:
------------------------------------

In shifted mode, time appears to be shifted from the current time.

    >>> from timemachine import machine as datetime
    >>> datetime.start_shift_by_delta(years=-1) # Last year.
    # Assuming that utcnow() returns 1 sec. to Christmas in 2010...
    >>> print datetime.datetime.utcnow()
#REVIEW: Shouldn't this be datetime.datetime(2010, 12, 24, 23, 59, 59, ...)    
    datetime.datetime(2009, 12, 25, 23, 59, 59, ...)
    >>> sleep(30) #30 seconds
    >>> print datetime.datetime.utcnow()
#REVIEW: Shouldn't this be datetime.datetime(2010, 12, 25, 23, 59, 59, ...)    
    datetime.datetime(2009, 12, 26, 00, 00, 29, ...)
#REVIEW: Do you want to add something about calling the shifted delta function?
    
    
Note about 'time' and other modules
-----------------------------------

This module does not handle any of Python's standard 'time' module.
If you use any of these calls to 'time', then this module will not help you.
(#TODO: Maybe write some functions to help?)
"""
import datetime as _datetime #python's standard datetime module
import time as _time #python's standard time module, needed for frozen time

# Attributes we just pass along from the standard datetime module:
MAXYEAR = _datetime.MAXYEAR
MINYEAR = _datetime.MINYEAR
# Not sure what this does, but let's pass it along anyway:
datetime_CAPI = _datetime.datetime_CAPI
# Classes that are passed-thru as-is:
time = _datetime.time
timedelta = _datetime.timedelta
tzinfo = _datetime.tzinfo

# Time machine control constants and variables:
_PRESENT_MODE = 0
_FROZEN_MODE = 1
_SHIFTED_MODE = 2
_mode = _PRESENT_MODE
# Frozen time variables:
_frozen_datetime = None
_frozen_utc_delta = None
# Shifted time variables:
_shifted_delta = None

def _is_present():
    global _mode
    return (_mode == _PRESENT_MODE)

def _is_frozen():
    global _mode
    return (_mode == _FROZEN_MODE)

def _is_shifted():
    global _mode
    return (_mode == _SHIFTED_MODE)

def return_to_present():
    """ Resets all time modes and resumes standard datetime operation. """
    global _mode
    global _frozen_datetime
    global _frozen_utc_delta
    global _shifted_delta
    _mode = _PRESENT_MODE
    _frozen_datetime = None
    _shifted_delta = None

def start_freeze_at_datetime(frozen):
    """
    Set the machine to a specific frozen time.
    If frozen includes a tzinfo, that tzinfo will be ignored;
    in other words, the machine is time-zone ignorant, just like all the
    classmethods in the standard datetime package.
    """
    global _mode
    global _frozen_datetime
    global _frozen_utc_delta
    return_to_present()
    _mode = _FROZEN_MODE
    # VERY IMPORTANT: _frozen_datetime must be a standard python datetime!
    # Otherwise, you get recursion errors later.
    _frozen_datetime = _datetime.datetime(
        frozen.year, frozen.month, frozen.day,
        frozen.hour, frozen.minute, frozen.second,
        frozen.microsecond)
    # Base UTC offset on the current system offset; it's not as accurate as
    # it could be, esp. for some frozen dates, but we're kinda stuck.
    # We could use pytz to implement a more elegant solution, but let's see
    # what happens for now.
    if _time.daylight == 1:
        _frozen_utc_delta = timedelta(seconds=_time.altzone)
    else:
        _frozen_utc_delta = timedelta(seconds=_time.timezone)

def start_freeze_by_delta(delta):
    #REVIEW: Shouldn't this be based on the present utcnow?
    calculated = _datetime.datetime.now() + delta
    start_freeze_at_datetime(calculated)

def start_freeze_now():
    #REVIEW: Wouldn't it be better to have a start_freeze_utcnow()?
    """ Freeze time starting at the *real* now. """
    start_freeze_at_datetime(_datetime.datetime.now())

def move_freeze_by_delta(delta):
    global _mode
    global _frozen_datetime
    assert (_mode == _FROZEN_MODE), 'Cannot increment unless in frozen mode!'
    _frozen_datetime = _frozen_datetime + delta

def start_shift_by_delta(delta):
    global _mode
    global _shifted_delta
    _mode = _SHIFTED_MODE
    _shifted_delta = delta

def start_shift_at_datetime(shifted_datetime):
    #REVIEW: Shouldn't this be based on the present utcnow?
    calcdelta = shifted_datetime - _datetime.datetime.now()
    start_shift_by_delta(calcdelta)

# Our own classes that override the standard datetime module:
# NOTE: I hope this doesn't mess up the object signatures, if anyone is checking.
class datetime(_datetime.datetime):
    @classmethod
    def now(cls, tz=None):
        if _is_frozen():
            return _frozen_datetime # Accomodate tz?
        elif _is_shifted():
            return _datetime.datetime.now(tz) + _shifted_delta
        else:
            return _datetime.datetime.now(tz)

    @classmethod
    def today(cls):
        if _is_frozen():
            return _frozen_datetime
        elif _is_shifted():
            return _datetime.datetime.today() + _shifted_delta
        else:
            return _datetime.datetime.today()

    @classmethod
    def utcnow(cls):
        if _is_frozen():
            return _frozen_datetime + _frozen_utc_delta
        elif _is_shifted():
            return _datetime.datetime.utcnow() + _shifted_delta
        else:
            return _datetime.datetime.utcnow()

class date(_datetime.date):
    @classmethod
    def today(cls):
        rpt = datetime.today()
        # Return report_date as a date:
        report_date = date(rpt.year, rpt.month, rpt.day)
        return report_date

def _proof(when):
    print "@ %s:" % when
    print "date.today()      :", date.today()
    print "datetime.today()  :", datetime.today()
    print "datetime.now()    :", datetime.now()
    print "datetime.utcnow() :", datetime.utcnow()

def _sanity_check():
    # This is some proof-of-concept code.
    _proof('Present')
    start_freeze_at_datetime(datetime(2010,12,25,23,45,56))
    _proof('Frozen')
    start_shift_by_delta(timedelta(days=-5))
    _proof('Shifted')

if __name__=="__main__":
    _sanity_check()