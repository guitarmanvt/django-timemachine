"""
Test the "edge cases" of the machine module.
"""
import datetime # for reference
import unittest
import machine
from time import sleep

class TestBaseClasses(unittest.TestCase):
    """
    Test things that machine inherits or passes through as-is from datetime.
    """
    def test_timedelta(self):
        """ timedelta objects should be identical. """
        self.assertEqual(machine.timedelta(seconds=1),
                         datetime.timedelta(seconds=1))

    def test_tzinfo(self):
        """ tzinfo objects should be identical. """
        # We're not actually testing this, because it's a abstract class.


class TestPassThruMode(unittest.TestCase):
    def test_time_passes(self):
        machine.set_passthru_mode()
        x = machine.datetime.utcnow()
        sleep(1)
        y = machine.datetime.utcnow()
        self.assertTrue(x < y, 'Prior time is not before later time.')

class TestFixedMode(unittest.TestCase):
    def test_time_on_hold(self):
        """ Time stands still in fixed mode. """
        machine.set_fixed_mode(2010, 12, 25, 23, 59, 59) # 1 sec. to Santa! :)
        x = machine.datetime.utcnow()
        sleep(1)
        y = machine.datetime.utcnow()
        self.assertEqual(x, y)

    def test_increment(self):
        machine.set_fixed_mode(2010, 12, 25, 23, 59, 59) # 1 sec. to Santa! :)
        x = machine.datetime.utcnow()
        sleep(1)
        machine.increment_fixed_mode(days=1)
        y = machine.datetime.utcnow()
        expected = (x + datetime.timedelta(days=1))
        self.assertEqual(y, expected, 'Incremented time is one day later, as expected.')

class TestOffsetMode(unittest.TestCase):
    def test_offset_works(self):
        machine.set_passthru_mode()
        x = machine.datetime.utcnow()
        machine.set_offset_mode(days=1)
        y = machine.datetime.utcnow()
        expected = x + datetime.timedelta(days=1)
        # OK, this assertion isn't coded right, but here's the idea:
        self.assertAlmostEqual(y, expected)

class TestModeSwitching(unittest.TestCase):
    def test_passthru_fixed_passthru(self):
        machine.set_passthru_mode()
        x = machine.datetime.utcnow()
        if 0: assert isinstance(x, datetime.datetime) #4cc
        machine.set_fixed_mode(x.year, x.month, x.day, x.hour, x.minute,
                               x.second, x.microsecond, x.tzinfo)
        sleep(1)
        y = machine.datetime.utcnow()
        sleep(1)
        z = machine.datetime.utcnow()
        machine.set_passthru_mode()
        sleep(1)
        w = machine.datetime.utcnow()
        self.assertTrue(x < y)
        self.assertEqual(y, z)
        self.assertTrue(z < w)

if __name__=='__main__':
    unittest.main()