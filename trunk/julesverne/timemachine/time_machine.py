"""
    Contains a class called datetime that is intended to be a drop in for python's
    standard datetime class.
   
    Its main purpose is to allow the developer to run code that "pretends" the
        current time (datetime.now()) is something different than it 
        actually is and see how the code functions in relation to the 
        developer-defined time.
   
    If __in_time_machine_mode is False, it just returns pythons's datetime
        return values.
       
   Otherwise, ...
        the method __set_dynamic_utc_datetime(in_datetime, now_utc_offset), will  
            set __in_time_machine_mode to True, 
            set __in_static_mode to False, 
            set __start_py_datetime_utc to the current python utcnow(),
            set __start_tm_datetime_utc to in_datetime, and

            if now_utc_offset is None, 
                set __start_tm_datetime to in_datetime plus the difference between 
                    python's datetime.now() and datetime.utcnow().
            If now_utc_offset is between -13 and 12 (inclusive),    
                set __start_tm_datetime to in_datetime plus 
                    timedelta(hours=now_utc_offset)                
                
            Then, 
                this module's datetime.utcnow() will return the datetime that
                    is equal to __start_tm_datetime_utc plus the amount of time
                    that has elapsed since it was last set, and 
                this module's datetime.now() will return the datetime that 
                    is equal to __start_tm_datetime plus the amount of time
                    that has elapsed since it was last set.
                        
        -- and/or --
        
        the method __set_static_utc_datetime(in_datetime, now_utc_offset) will
            set __in_time_machine_mode to True,
            set __in_static_mode to True, and            
            
            if now_utc_offset is None, 
                this module's datetime.utcnow() will return in_datetime, and
                this module's datetime.now() will return in_datetime plus
                    the difference between python's datetime.now() and 
                    datetime.utcnow().
            
            If now_utc_offset is between -13 and 12 (inclusive),
                this module's datetime.utcnow() will return in_datetime, and
                this module's datetime.now() will return in_datetime plus 
                    timedelta(hours=now_utc_offset)
       
"""

from datetime import datetime as py_datetime
from datetime import timedelta


def round_to_seconds(in_datetime):
    """
    Round a datetime value to seconds.
    """
    dt = in_datetime

    if dt.microsecond < 500000:
        return dt.replace(microsecond=0)

    dt = dt + timedelta(seconds = 1)
    return dt.replace(microsecond=0)


class datetime():
    """
    Object that mimics python's datetime module, but with a user provided datetime
    """

    __in_static_mode = False
    __in_time_machine_mode = False
    
    # python's datetime setting for when __in_time_machine_mode gets set to True
    __start_py_datetime_utc = py_datetime.utcnow()
    
    # timemachine's datetime setting for when __in_time_machine_mode set to True
    __start_tm_datetime_utc = py_datetime.utcnow()
    __start_tm_datetime = py_datetime.now()    
    
    @classmethod
    def __validate_now_utc_offset(cls, now_utc_offset):
        if now_utc_offset < -13 or now_utc_offset > 12:
            raise ValueError('now_utc_offset must be between -13 and 12.')
        if type(now_utc_offset) <> int:
            raise ValueError('now_utc_offset must be an integer.')
        return

    @classmethod        
    def __set_new_time(cls, in_datetime, now_utc_offset):
        cls.__start_py_datetime_utc = py_datetime.utcnow()
        cls.__start_tm_datetime_utc = in_datetime
 
        if now_utc_offset is not None:
            cls.__validate_now_utc_offset(now_utc_offset)
            cls.__start_tm_datetime = in_datetime + timedelta(hours=now_utc_offset)            
        else:
            rounded_now = round_to_seconds(py_datetime.now())
            rounded_utcnow = round_to_seconds(py_datetime.utcnow())
            time_difference  = rounded_now - rounded_utcnow
            cls.__start_tm_datetime = in_datetime + time_difference
    
    @classmethod
    def now(cls):
        if cls.__in_time_machine_mode:
            if cls.__in_static_mode:
                return cls.__start_tm_datetime

            # how long since time_machine mode was started                
            time_difference = py_datetime.utcnow() - cls.__start_py_datetime_utc
            return cls.__start_tm_datetime + time_difference
            
        return py_datetime.now()

    @classmethod
    def utcnow(cls):
        if cls.__in_time_machine_mode:
            if cls.__in_static_mode:
                return cls.__start_tm_datetime_utc
            
            # how long since time_machine mode was started
            time_difference = py_datetime.utcnow() - cls.__start_py_datetime_utc
            return cls.__start_tm_datetime_utc + time_difference
            
        return py_datetime.utcnow()

        
    @classmethod
    def stop_time_machine_mode(cls):
        cls.__in_time_machine_mode = False   

    @classmethod
    def in_time_machine_mode(cls):
        return cls.__in_time_machine_mode

    @classmethod
    def in_static_mode(cls):
        return cls.__in_static_mode
        
    @classmethod
    def set_dynamic_utc_datetime(cls, in_datetime, now_utc_offset=None):
    
        cls.__set_new_time(in_datetime, now_utc_offset)                
        cls.__in_time_machine_mode = True
        cls.__in_static_mode = False
       
    @classmethod
    def set_static_utc_datetime(cls, in_datetime, now_utc_offset=None):

        cls.__set_new_time(in_datetime, now_utc_offset)                
        cls.__in_time_machine_mode = True
        cls.__in_static_mode = True

        
      
