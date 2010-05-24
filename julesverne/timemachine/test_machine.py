"""
Test the "edge cases" of the machine module.
"""

#REVIEW To be a little more rigorous, shouldn't this also be testing
# an external module that uses machine.datetime?

import unittest
from machine import *
from time import sleep

christmas = datetime(2010, 12, 24, 23, 59, 59) # almost Christmas! :)

def nearly_simultaneous(datetime1, datetime2,
                        tolerance=timedelta(microseconds=500000)):
    """
    Returns True if datetimes are within tolerance (in microseconds) of each
    other.
    """
    if tolerance.days < 0:
        tolerance *= -1
    diff = (datetime1 - datetime2)
    if diff.days < 0:
        diff *= -1
    return (diff < tolerance)

class Test(unittest.TestCase):
    """ Test support functions. """
#REVIEW: Do you not want to test it for cases when you pass in 
#        a timedelta, a negative time_delta and for cases when 
#        the second time is less than the first time?
    def test_nearly_simultaneous_true(self):
        a = datetime.now()
        sleep(0.4)
        b = datetime.now()
        self.assertTrue(nearly_simultaneous(a, b))

    def test_nearly_simultaneous_false(self):
        a = datetime(2010,12,25)
        b = a + timedelta(seconds=1)
        self.assertFalse(nearly_simultaneous(a, b))

class TestPresentTime(unittest.TestCase):
    def test_time_passes(self):
        return_to_present()
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        self.assertTrue(x < y, 'Prior time is not before later time.')

class TestFrozenTime(unittest.TestCase):
    def test_freeze_on_datetime(self):
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        #REVIEW: Don't you want to test in regard to christmas?        
        self.assertEqual(x, y)

    def test_freeze_by_delta(self):
        #REVIEW: Don't you want to test in regard to the present now()?    
        start_freeze_by_delta(timedelta(hours=-5))
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        self.assertEqual(x, y)

    def test_increment(self):
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        move_freeze_by_delta(timedelta(days=1))
        y = datetime.now()
        expected = (x + timedelta(days=1))
        #REVIEW: Shouldn't the string be opposite of what's expected, in order 
        #        to explain a test error?
        self.assertEqual(y, expected, 'Incremented time is one day later, as expected.')


    def test_freeze_now(self):
        return_to_present()
        u = datetime.now()
        start_freeze_now()
        w = datetime.now()
        sleep(1)
        x = datetime.now()
        self.assertTrue(nearly_simultaneous(u, w))
        self.assertEqual(w, x)

    def test_utc_now(self):
        " utcnow reports different offset during frozen time than present time "
        return_to_present()
        a = datetime.now()
        b = datetime.utcnow()
        start_freeze_at_datetime(christmas)
        c = datetime.now()
        d = datetime.utcnow()
        after = (d - c)
        e = a + after
        self.assertTrue(nearly_simultaneous(b, e))

class TestShiftedTime(unittest.TestCase):
    def test_shift_by_datetime(self):
        start_shift_at_datetime(christmas)
        y = datetime.now()
        sleep(1)
        z = datetime.now()
        self.assertTrue(y < z)
        self.assertEqual(z.day, 25)
        self.assertEqual(z.hour, 0)
        self.assertEqual(z.minute, 0)

    def test_shift_by_delta(self):
        return_to_present()
        x = datetime.now()
        start_shift_by_delta(timedelta(days=1))
        y = datetime.now()
        expected = x + timedelta(days=1)
        self.assertTrue(nearly_simultaneous(y, expected))

    def test_utc_now(self):
        " utcnow reports different offset during shifted time than present time "
        return_to_present()
        a = datetime.now()
        b = datetime.utcnow()
        start_shift_at_datetime(christmas)
        c = datetime.now()
        d = datetime.utcnow()
        after = (d - c)
        e = a + after
        self.assertTrue(nearly_simultaneous(b, e))

class TestTimeTravel(unittest.TestCase):
    " Test switching between various time modes."

    def test_present_frozen_present(self):
        return_to_present()
        u = datetime.now()
        start_freeze_now()
        sleep(1)
        w = datetime.now()
        sleep(1)
        x = datetime.now()
        return_to_present()
        sleep(1)
        y = datetime.now()
        self.assertTrue(nearly_simultaneous(u, w))
        self.assertEqual(w, x)
        #should be ~3 seconds difference
        #REVIEW: Shouldn't this be (u, y, ...)
        self.assertTrue(nearly_simultaneous(x, y, timedelta(seconds=3.1)))
        #REVIEW: How about timedelta(seconds = 3) <= y - u <= timedelta(seconds = 4)

if __name__=='__main__':
    unittest.main()