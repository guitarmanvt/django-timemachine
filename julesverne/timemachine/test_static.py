#REVIEW: Rework tests so that they individually finish in < 3 seconds each.
#        Otherwise, person running tests will think they're timing out.
#RESPONSE: These three tests only take 7 seconds to run all together.
from time import sleep
import unittest

from datetime import timedelta
from datetime import datetime as py_datetime
from time_machine import datetime, round_to_seconds


def set_alternative_datetimes():
    alt_dts = []

    for hours in range(0, 24):
        for minutes in range(0, 60):
            alt_dts.append(py_datetime(2010, 2, 10, hours, minutes))

    return alt_dts


def t_timemachine_static_mode_simple(self):
    """
    Make sure that module works for in_static_mode = True and no now vs. utc offset
    """
    datetime.stop_time_machine_mode()
    datetimes = set_alternative_datetimes()

    # avoid slight differences in the timing of capturing now() and utcnow()
    now = round_to_seconds(py_datetime.now())
    utcnow = round_to_seconds(py_datetime.utcnow())
    now_minus_utc = now - utcnow

    for d_time in datetimes:
        datetime.set_static_utc_datetime(d_time)
        tm_utcnow = datetime.utcnow()
        self.assertEqual(tm_utcnow, d_time)

        expected_now = d_time + now_minus_utc
        tm_now = datetime.now()
        self.assertEqual(tm_now, expected_now)

        if d_time.minute == 0: sleep(.2)

    self.assertEqual(datetime.in_static_mode(), True)
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, True)

    datetime.stop_time_machine_mode()
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, False)


def t_timemachine_static_mode_offset(self):
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
        ( py_datetime(2008, 1, 1, 0, 0, 0), -5,
                            py_datetime(2007, 12, 31, 19, 0, 0)),
        ( py_datetime(2008, 1, 1, 0, 0, 0), 0,
                            py_datetime(2008, 1, 1, 0, 0, 0)),
        ( py_datetime(2008, 1, 1, 0, 0, 0), 5,
                            py_datetime(2008, 1, 1, 5, 0, 0)),
        ( py_datetime(2008, 1, 1, 0, 0, 0), 12,
                            py_datetime(2008, 1, 1, 12, 0, 0)),

        ( py_datetime(2009, 9, 1, 4, 6, 7), -13,
                            py_datetime(2009, 8, 31, 15, 6, 7)),
        ( py_datetime(2009, 9, 1, 4, 6, 7), -5,
                            py_datetime(2009, 8, 31, 23, 6, 7)),
        ( py_datetime(2009, 9, 1, 4, 6, 7), 0,
                            py_datetime(2009, 9, 1, 4, 6, 7)),
        ( py_datetime(2009, 9, 1, 4, 6, 7), 5,
                            py_datetime(2009, 9, 1, 9, 6, 7)),
        ( py_datetime(2009, 9, 1, 4, 6, 7), 12,
                            py_datetime(2009, 9, 1, 16, 6, 7)),

        ( py_datetime(2010, 8, 9, 5, 59, 59), -13,
                            py_datetime(2010, 8, 8, 16, 59, 59)),
        ( py_datetime(2010, 8, 9, 5, 59, 59), -5,
                            py_datetime(2010, 8, 9, 0, 59, 59)),
        ( py_datetime(2010, 8, 9, 5, 59, 59), 0,
                            py_datetime(2010, 8, 9, 5, 59, 59)),
        ( py_datetime(2010, 8, 9, 5, 59, 59), 5,
                            py_datetime(2010, 8, 9, 10, 59, 59)),
        ( py_datetime(2010, 8, 9, 5, 59, 59), 12,
                            py_datetime(2010, 8, 9, 17, 59, 59)),

        ( py_datetime(2011, 12, 31, 20, 59, 59), -13,
                            py_datetime(2011, 12, 31, 7, 59, 59)),
        ( py_datetime(2011, 12, 31, 20, 59, 59), -5,
                            py_datetime(2011, 12, 31, 15, 59, 59)),
        ( py_datetime(2011, 12, 31, 20, 59, 59), 0,
                            py_datetime(2011, 12, 31, 20, 59, 59)),
        ( py_datetime(2011, 12, 31, 20, 59, 59), 5,
                            py_datetime(2012, 1, 1, 1, 59, 59)),
        ( py_datetime(2011, 12, 31, 20, 59, 59), 12,
                            py_datetime(2012, 1, 1, 8, 59, 59)),
        ]

    datetime.stop_time_machine_mode()

    for test_data in test_dtimes:
        test_dtime = test_data[0]
        datetime.set_static_utc_datetime(
            test_dtime,
            now_utc_offset = test_data[1]
           )

        self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)

        expected_now = test_data[2]
        self.assertEqual(round_to_seconds(datetime.now()), expected_now)

    sleep(2)
    self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)

    self.assertEqual(datetime.in_static_mode(), True)
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, True)

    datetime.stop_time_machine_mode()
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, False)

def t_round_to_secs(self):

    test_datetimes = []

    for days in [1, 15, 31]:
        for hours in [0, 12, 23]:
            for minutes in [0, 30, 59]:
                for seconds in [0, 30, 59]:
                    for microseconds in [0, 499999, 500000, 500001, 999999]:
                        test_datetimes.append( py_datetime(2010, 1,
                            days,
                            hours,
                            minutes,
                            seconds,
                            microseconds
                           )
                          )

    expected_datetimes =[]

    for days in [1, 15, 31]:
        for hours in [0, 12, 23]:
            for minutes in [0, 30, 59]:
                for seconds in [0, 30, 59]:
                    for microseconds in [0, 499999, 500000, 500001, 999999]:

                        # check if rounding up
                        if microseconds >= 500000:
                            if seconds == 59 and minutes == 59 and \
                              hours == 23 and days == 31:
                                # Jan 31, 23:59:59 --> Feb 1, 00:00:00
                                expected_datetimes.append(
                                    py_datetime(2010, 2, 1, 0,0,0,0)
                                   )
                            elif seconds == 59 and minutes == 59 and \
                              hours == 23:
                                expected_datetimes.append(
                                    py_datetime(2010, 1, days + 1, 0,0,0,0)
                                   )
                            elif seconds == 59 and minutes == 59:
                                expected_datetimes.append(
                                    py_datetime(2010, 1, days, hours + 1,0,0,0)
                                   )
                            elif seconds == 59:
                                expected_datetimes.append(
                                    py_datetime(2010, 1, days, hours,
                                              minutes + 1,0,0)
                                   )
                            else:
                                expected_datetimes.append(
                                    py_datetime(2010, 1, days, hours,
                                             minutes, seconds + 1,0)
                                   )
                        else: # round down
                            expected_datetimes.append(
                                py_datetime(2010, 1, days, hours,
                                         minutes, seconds,0)
                               )

    self.assertEqual(len(test_datetimes), len(expected_datetimes))

    for index in range(len(test_datetimes)):
        rounded_dt = round_to_seconds(test_datetimes[index])
        self.assertEqual(rounded_dt, expected_datetimes[index])




class TestTimeMachineStatic(unittest.TestCase):

    def test_timemachine_static_mode_simple(self):
        t_timemachine_static_mode_simple(self)

    def test_timemachine_static_mode_offset(self):
        t_timemachine_static_mode_offset(self)

    def test_round_to_seconds(self):
        t_round_to_secs(self)


if __name__ == "__main__":
    unittest.main()