"""
Test the "edge cases" of the machine module.
"""

#REVIEW To be a little more rigorous, shouldn't this also be testing
# an external module that uses machine.datetime?
#RESPONSE: I'm not testing python's import statements, so I don't think so.
#          If we find a case where something weird happens, we'll add a test
#          for it later. Good thought, anyway.

import unittest
from machine import *
from time import sleep
from utils import nearly_simultaneous

christmas = datetime(2009, 12, 24, 23, 59, 59) # almost Christmas! :)

class TestPresentTime(unittest.TestCase):
    def test_time_passes(self):
        return_to_present()
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        self.assertTrue(x < y, 'Prior time is not before later time.')

class TestFrozenTime(unittest.TestCase):
    def test_freeze_on_datetime_start(self):
        """ Freeze on datetime did not start at the right time. """
        return_to_present()
        x = datetime.now()
        start_freeze_at_datetime(christmas)
        y = datetime.now()
        self.assertFalse(nearly_simultaneous(x, y))
        self.assertTrue(nearly_simultaneous(y, christmas))

    def test_freeze_by_delta_start(self):
        """ Freeze by delta did not start at the right time. """
        delta = timedelta(hours=-5)
        return_to_present()
        x = datetime.now()
        start_freeze_by_delta(delta)
        y = datetime.now()
        z = x + delta
        self.assertTrue(nearly_simultaneous(y, z))

    def test_freeze_now_start(self):
        """ Freeze by delta did not start at the right time. """
        return_to_present()
        u = datetime.now()
        start_freeze_now()
        w = datetime.now()
        self.assertTrue(nearly_simultaneous(u, w))

    def test_freeze_without_move(self):
        """ Frozen time without move did not stay constant. """
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        self.assertEqual(x, y)
        # NOTE: This is not comparing to 'christmas', because that's
        # already covered in test_freeze_on_datetime().

    def test_move_negative(self):
        """ Frozen time did not move correctly with negative delta. """
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        move_freeze_by_delta(timedelta(days=-1))
        y = datetime.now()
        expected = (x + timedelta(days=-1))
        self.assertEqual(y, expected)

    def test_move_positive(self):
        """ Frozen time did not move correctly with positive delta. """
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        move_freeze_by_delta(timedelta(days=1))
        y = datetime.now()
        expected = (x + timedelta(days=1))
        self.assertEqual(y, expected)

    def test_move_zero(self):
        """ Frozen time did not remain constant with zero delta. """
        start_freeze_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        move_freeze_by_delta(timedelta())
        y = datetime.now()
        self.assertEqual(x, y)

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
    def test_shift_by_datetime_start(self):
        """ Shifted time did not start at the specified datetime. """
        return_to_present()
        start_shift_at_datetime(christmas)
        y = datetime.now()
        self.assertTrue(nearly_simultaneous(y, christmas))

    def test_shift_by_delta_start(self):
        """ Shifted time did not start at the specified delta. """
        return_to_present()
        x = datetime.now()
        start_shift_by_delta(timedelta(days=1))
        y = datetime.now()
        expected = x + timedelta(days=1)
        self.assertTrue(nearly_simultaneous(y, expected))

    def test_shifted_time_moves(self):
        """ Shifted time is not moving in parallel with normal time. """
        return_to_present()
        start_shift_at_datetime(christmas)
        x = datetime.now()
        sleep(1)
        y = datetime.now()
        expected = x + timedelta(seconds=1)
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
        normal_start = datetime.now()
        start_freeze_now()
        sleep(1)
        frozen1 = datetime.now()
        sleep(1)
        frozen2 = datetime.now()
        return_to_present()
        sleep(1)
        back_to_normal = datetime.now()
        expected = normal_start + timedelta(seconds=3)
        self.assertTrue(nearly_simultaneous(normal_start, frozen1))
        self.assertEqual(frozen1, frozen2)
        self.assertTrue(nearly_simultaneous(back_to_normal, expected))

if __name__=='__main__':
    unittest.main()