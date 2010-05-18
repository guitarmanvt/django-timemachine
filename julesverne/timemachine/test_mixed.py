#REVIEW: Rework tests so that they individually finish in < 3 seconds each.
#        Otherwise, person running tests will think they're timing out.

from time import sleep
import unittest

from datetime import timedelta
from datetime import datetime as py_datetime
from time_machine import datetime, round_to_seconds




def t_timemachine_mode_false(self):
    """
    Make sure that module works for in_timemachine_mode = False
    """
    self.assertEqual(1, 1)

    datetime.stop_time_machine_mode()
    now = round_to_seconds(py_datetime.now())
    tm_now = round_to_seconds(datetime.now())
    self.assertEqual(tm_now, now)

    utcnow = round_to_seconds(py_datetime.utcnow())
    tm_utcnow = round_to_seconds(datetime.utcnow())
    self.assertEqual(tm_utcnow, utcnow)
    sleep(2)

    now = round_to_seconds(py_datetime.now())
    tm_now = round_to_seconds(datetime.now())
    self.assertEqual(tm_now, now)

    utcnow = round_to_seconds(py_datetime.utcnow())
    tm_utcnow = round_to_seconds(datetime.utcnow())
    self.assertEqual(tm_utcnow, utcnow)

    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, False)



def t_timemachine_mixed(self):
    """
    Make sure that module works for in_static_mode = True and with now vs. utc offset
    """
    datetime.stop_time_machine_mode()

    # Test for catching bad offest errors
    try:
        datetime.set_static_utc_datetime(
                py_datetime(2008, 1, 1, 0, 0, 0, 0),
                now_utc_offset = -14
               )
    except ValueError, e:
        self.assertEqual(e[0], 'now_utc_offset must be between -13 and 12.')

    try:
        datetime.set_static_utc_datetime(
                py_datetime(2008, 1, 1, 0, 0, 0, 0),
                now_utc_offset = 2.4
               )
    except ValueError, e:
        self.assertEqual(e[0], 'now_utc_offset must be an integer.')

    if 1: # to make this long section collapsible
        test_dtimes = [ # input_datetime, now_utc_offset, expected_now
        ( py_datetime(2008, 1, 1, 0, 0, 0), -13,
                            py_datetime(2007, 12, 31, 11, 0, 0)),

        ( py_datetime(2009, 9, 1, 4, 6, 7), -5,
                            py_datetime(2009, 8, 31, 23, 6, 7)),

        ( py_datetime(2010, 8, 9, 5, 59, 59), 0,
                            py_datetime(2010, 8, 9, 5, 59, 59)),

        ( py_datetime(2011, 12, 31, 20, 59, 59), 5,
                            py_datetime(2012, 1, 1, 1, 59, 59)),

        ]

    datetime.stop_time_machine_mode()

    # dynamic
    test_dtime = test_dtimes[0][0]
    datetime.set_dynamic_utc_datetime(
        test_dtime,
        now_utc_offset = test_dtimes[0][1]
       )

    self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)

    expected_now = test_dtimes[0][2]
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)

    sleep(2)
    expected_utcnow = test_dtime + timedelta(seconds = 2)
    self.assertEqual(round_to_seconds(datetime.utcnow()),expected_utcnow)

    expected_now += timedelta(seconds = 2)
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)
    #print "\r %s %s            " %(test_dtime, test_dtimes[0][1]),

    # static
    test_dtime = test_dtimes[1][0]
    datetime.set_static_utc_datetime(
        test_dtime,
        now_utc_offset = test_dtimes[1][1]
       )

    self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)

    expected_now = test_dtimes[1][2]
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)

    sleep(2)
    self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)
    #print "\r %s %s            " %(test_dtime, test_dtimes[1][1]),

    # dynamic
    test_dtime = test_dtimes[2][0]
    datetime.set_dynamic_utc_datetime(
        test_dtime,
        now_utc_offset = test_dtimes[2][1]
       )

    self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)

    expected_now = test_dtimes[2][2]
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)

    sleep(2)
    expected_utcnow = test_dtime + timedelta(seconds = 2)
    self.assertEqual(round_to_seconds(datetime.utcnow()),expected_utcnow)

    expected_now += timedelta(seconds = 2)
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)
    #print "\r %s %s            " %(test_dtime, test_dtimes[2][1]),

    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, True)

    # turn off time machine
    datetime.stop_time_machine_mode()
    now = round_to_seconds(py_datetime.now())
    tm_now = round_to_seconds(datetime.now())
    self.assertEqual(tm_now, now)

    utcnow = round_to_seconds(py_datetime.utcnow())
    tm_utcnow = round_to_seconds(datetime.utcnow())
    self.assertEqual(tm_utcnow, utcnow)

    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, False)


class TestTimeMachineMixed(unittest.TestCase):

    def test_timemachine_mode_false(self):
        t_timemachine_mode_false(self)

    def test_timemachine_mixed(self):
        t_timemachine_mixed(self)


if __name__ == "__main__":
    unittest.main()