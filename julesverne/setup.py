#!/usr/bin/env python
"""
Distutils Setup Script for the timemachine package.
NOTE: Not truly a part of the Django app "julesverne", but it's in this folder
      for ease of development by the developers (us).
"""

from distutils.core import setup

setup(name='TimeMachine',
      version='1.0',
      description="drop-in replacement for python's standard datetime package",
      maintainer_email='guitarman@vt.edu',
      url='http://code.google.com/p/django-timemachine/',
      packages=['timemachine'],
     )
