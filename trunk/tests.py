"""
Consolidated tests.
Copyright (c) 2010 
"""

import unittest
from test_time_machine_dynamic import *
from test_time_machine_static import *
from test_time_machine_mixed import *

print 
suite = unittest.TestLoader().loadTestsFromTestCase(TestTimeMachineStatic)
unittest.TextTestRunner(verbosity=2).run(suite)

suite = unittest.TestLoader().loadTestsFromTestCase(TestTimeMachineDynamic)
unittest.TextTestRunner(verbosity=2).run(suite)
 
suite = unittest.TestLoader().loadTestsFromTestCase(TestTimeMachineMixed)
unittest.TextTestRunner(verbosity=2).run(suite)
print
