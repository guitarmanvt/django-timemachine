julesverne django app
=====================

The julesverne django app "wraps" the timemachine package, so you can see how
to use it in a Django project.

#TODO: Finish this example app.

About setup.py and non-Django timemachine installation
------------------------------------------------------

This is the DistUtils setup script for the "timemachine" package. It's not a
part of the julesverne django app, but it is in this folder for convenience.

You can use setup.py to install the "timemachine" package into your python
installation, without installing/using django.  Just do this (as root):

# cd /path/to/julesverne
# python setup.py install

Then, you'll be able to do this in python:

>>> import timemachine