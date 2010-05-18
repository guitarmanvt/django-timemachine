#REVIEW: Rework tests so that they individually finish in < 3 seconds each.
#        Otherwise, person running tests will think they're timing out.

from time import sleep
import unittest

from datetime import timedelta
from datetime import datetime as py_datetime
from time_machine import datetime, round_to_seconds


DATETIMES = []

for month in [1, 12]:
    for day in [1, 31]:
        for hour in [0, 12, 23]:
            for minute in [0, 59]:
                for second in [0, 59]:
                    DATETIMES.append(py_datetime(2010, month, day,
                                               hour, minute, second))

DT_INDEX = 0
DT_INTERVAL = 1

if 1: # to make this long section collapsible
    OFFSET_DTS = [ # input_datetime, now_utc_offset, expected_now
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

OFFSET_INDEX = 0
OFFSET_INTERVAL = 1    


def t_timemachine_dynamic_mode_simple(self):
    """
    Make sure that module works for in_static_mode = False and no now vs. utc offset
    """
    global DATETIMES
    global DT_INDEX
    global DT_INTERVAL
    
    datetime.stop_time_machine_mode()


    # avoid slight differences in the timing of capturing now() and utcnow()
    now = round_to_seconds(py_datetime.now())
    utcnow = round_to_seconds(py_datetime.utcnow())
    now_minus_utc = now - utcnow
    
    datetimes = DATETIMES[DT_INDEX:DT_INDEX+DT_INTERVAL]
    DT_INDEX += 1

    for d_time in datetimes:
        #print "\rtesting %s" % d_time.strftime("%m %d %H:%M:%S"),
        datetime.set_dynamic_utc_datetime(d_time)
        tm_utcnow = datetime.utcnow()

        self.assertEqual(tm_utcnow, d_time)

        expected_now = d_time + now_minus_utc
        tm_now = round_to_seconds(datetime.now())
        self.assertEqual(tm_now, expected_now)

        sleep(2)

        expected_utcnow = d_time + timedelta(seconds = 2)
        tm_utcnow = round_to_seconds(datetime.utcnow())
        self.assertEqual(tm_utcnow, expected_utcnow)

        expected_now += timedelta(seconds = 2)
        tm_now = round_to_seconds(datetime.now())
        self.assertEqual(tm_now, expected_now)

    self.assertEqual(datetime.in_static_mode(), False)
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, True)

    datetime.stop_time_machine_mode()
    in_tm_mode = datetime.in_time_machine_mode()
    self.assertEqual(in_tm_mode, False)


def t_timemachine_dynamic_mode_offset(self):
    """
    Make sure that module works for in_static_mode = True and with now vs. utc offset
    """
    datetime.stop_time_machine_mode()

    global OFFSET_DTS
    global OFFSET_INDEX
    global OFFSET_INTERVAL    
    
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

     
    datetime.stop_time_machine_mode()
    
    
    # [[input_datetime, now_utc_offset, expected_now], ]
    test_dtimes = OFFSET_DTS[OFFSET_INDEX:OFFSET_INDEX+OFFSET_INTERVAL]
    OFFSET_INDEX += 1
    
    for test_data in test_dtimes:
        test_dtime = test_data[0]
        datetime.set_dynamic_utc_datetime(
            test_dtime,
            now_utc_offset = test_data[1]
           )

        self.assertEqual(round_to_seconds(datetime.utcnow()), test_dtime)

        expected_now = test_data[2]
        self.assertEqual(round_to_seconds(datetime.now()), expected_now)

        sleep(2)
        expected_utcnow = test_dtime + timedelta(seconds = 2)
        self.assertEqual(round_to_seconds(datetime.utcnow()),expected_utcnow)

        expected_now += timedelta(seconds = 2)
        self.assertEqual(round_to_seconds(datetime.now()), expected_now)
        #print "\r %s %s            " %(test_dtime, test_data[1]),


    sleep(2)
    expected_utcnow = test_dtime + timedelta(seconds = 4)
    self.assertEqual(round_to_seconds(datetime.utcnow()),expected_utcnow)

    expected_now += timedelta(seconds = 2)
    self.assertEqual(round_to_seconds(datetime.now()), expected_now)




class TestTimeMachineDynamic(unittest.TestCase):    
    def test_timemachine_dynamic_mode_simple(self):
        t_timemachine_dynamic_mode_simple(self)    

    def test_timemachine_dynamic_mode_offset(self):
        t_timemachine_dynamic_mode_offset(self)



def suite():
    global DATETIMES 
    suite = unittest.TestSuite()
    
    for index in range(len(DATETIMES)):
        suite.addTest(TestTimeMachineDynamic(
            'test_timemachine_dynamic_mode_simple'))

    for index in range(len(OFFSET_DTS)):
        suite.addTest(TestTimeMachineDynamic(
            'test_timemachine_dynamic_mode_offset'))
    
    
    return suite

   
def test_main():
    testsuite = suite()
    runner = unittest.TextTestRunner()
    result = runner.run(testsuite)
     
if __name__ == "__main__":
    test_main()