timemachine package
===================
Drop-in replacement for Python's standard 'datetime' package and/or class.

A word about limitations
------------------------

The 'datetime' class in the python standard package should have been named
'DateTime', but it wasn't. Oh well. Consequently, we must continue the bad
naming practice for the timemachine's 'datetime' class.

Also, the standard 'datetime' package does not handle timezones very well.
It relies on the UTC offset from the standard python 'time' package. While
this works (sort-of), it's not sophisticated and has too much dependency on
the server clock. Oh well. Consequently, the timemachine has the same flaws
as the python standard package.

What this means is:
- The timemachine handles timezones the same way as the standard package.
- Alternate time modes are based on system local time, *NOT* on UTC time.
- The "utcnow()" function is based on the UTC offset *AT THE CURRENT LOCAL TIME
  WHEN THE ALTERNATE TIME MODE IS STARTED*. In other words, if you use for a
  long-running process that stays running across the Daylight Savings Time
  boundary, then you will get weird results. Just be prepared for that.
  Fortunately, most processes are milliseconds-long and won't bump into this.

Note about 'time' and other modules
-----------------------------------

This module does not handle any of Python's standard 'time' module.
If you use any of these calls to 'time', then this module will not help you.
(#TODO: Maybe write some functions to help?)

Importing the datetime package
------------------------------

Here are some examples using the datetime package:

    # If you're just importing the standard package:
    >>> import datetime

    # If you want to use the timemachine package instead:
    >>> from timemachine import machine as datetime

    # Then, your code can remain the same:
    >>> print datetime.datetime.now()

Importing just the datetime class
---------------------------------

Here's how you can import the 'datetime' class.

    # If you just want to import the standard 'datetime' class:
    >>> from datetime import datetime

    # If you want to use the timemachine's 'datetime' class:
    >>> from timemachine.machine import datetime

    # NOTE: You'll also need to import the machine module itself...
    >>> from timemachine import machine
    # ...so you can control the machine, like this:
    >>> machine.reset_to_present()

    # Then, your code can remain the same:
    >>> print datetime.now()

Using the timemachine 'present' mode:
---------------------------------------

Present mode makes the timemachine work exactly like the standard module.

    >>> from timemachine import machine as datetime
    >>> datetime.return_to_present() # this is actually the default mode
    >>> print datetime.datetime.now()

    (It will print the current local datetime.)

Using the timemachine 'frozen' mode:
-----------------------------------

Frozen mode makes the timemachine stay on a pre-set datetime.

    >>> from timemachine import machine as datetime
    >>> christmas = datetime.datetime(2010, 12, 24, 23, 59, 59) # almost! :)
    >>> datetime.start_freeze_at_datetime(christmas)
    >>> print datetime.datetime.now()
    datetime.datetime(2010, 12, 24, 23, 59, 59, ...)
    >>> sleep(30) #30 seconds of real time, which will be ignored
    >>> print datetime.datetime.now() # nothing changes...
    datetime.datetime(2010, 12, 24, 23, 59, 59, ...)
    >>> datetime.move_freeze_by_delta(timedelta(days=7)) # ...until you tell it
    >>> print datetime.datetime.now() # now it reports New Year's Eve! :)
    datetime.datetime(2010, 12, 31, 23, 59, 59, ...)

You can also freeze time based on a delta from the current real time:

    >>> from timemachine import machine as datetime
    >>> datetime.start_freeze_by_delta(timedelta(days=-1)) #Freeze yesterday.

You can also freeze time at the current moment in real time:

    >>> from timemachine import machine as datetime
    >>> datetime.start_freeze_now()

Using the timemachine 'shifted' mode:
------------------------------------

In shifted mode, time appears to be shifted from the current time.

    >>> from timemachine import machine as datetime
    >>> datetime.start_shift_by_delta(years=-1) # Last year.
    # Assuming that now() returns 1 sec. to Christmas in 2010...
    >>> print datetime.datetime.now()
    datetime.datetime(2009, 12, 24, 23, 59, 59, ...)
    >>> sleep(30) #30 seconds of real time, same as 30 seconds of shifted time
    >>> print datetime.datetime.now()
    datetime.datetime(2009, 12, 24, 00, 00, 29, ...)

You can also move to shifted time starting at a certain delta:

    >>> from timemachine import machine as datetime
    >>> datetime.start_shift_at_datetime(christmas) # Note this call.
    >>> print datetime.datetime.now()
    datetime.datetime(2010, 12, 24, 23, 59, 59, ...)
    >>> sleep(30) #30 seconds of real time, same as 30 seconds of shifted time
    >>> print datetime.datetime.now()
    datetime.datetime(2010, 12, 24, 00, 00, 29, ...)

FINIS.