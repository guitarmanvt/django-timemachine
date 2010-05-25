import unittest
from datetime import datetime, timedelta

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

class TestUtils(unittest.TestCase):
    """
    Test support function.
    Honestly, this might be a bit of TDD overkill, but why not?
    """
    def test_nearly_simultaneous_true(self):
        for secs in [0.4, -0.4, 0]:
            a = datetime.now()
            b = a + timedelta(seconds=secs)
            self.assertTrue(nearly_simultaneous(a, b))

    def test_nearly_simultaneous_false(self):
        for secs in [0.6, -0.6, 10000, -10000]:
            a = datetime.now()
            b = a + timedelta(seconds=secs)
            self.assertFalse(nearly_simultaneous(a, b))

if __name__=="__main__":
    unittest.main()