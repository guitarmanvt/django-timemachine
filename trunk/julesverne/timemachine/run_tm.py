import datetime
import time
from time_machine import TimeMachine


print "Start"
print "real now", datetime.datetime.now()
print
print "Initial TM mode", TimeMachine.in_time_machine_mode()
print "Initial TM now", TimeMachine.now()
print
print "Starting tm mode"
TimeMachine.start_time_machine_mode()
print "New TM mode", TimeMachine.in_time_machine_mode()
print
print "Giving alternative start time"
TimeMachine.set_alternative_datetime(datetime.datetime(2100, 1, 1))
print
print "New TM now", TimeMachine.now()
print 
print "Sleeping 3 seconds"
time.sleep(3)
print "New TM now", TimeMachine.now()
print
print "Stopping tm mode"
TimeMachine.stop_time_machine_mode()
print "Last TM now", TimeMachine.now()