import datetime


class TimeMachine():
    """
    Object that mimics python's datetime module, but with a user provided datetime
    """

    __in_static_mode = True
    __in_time_machine_mode = False
    
    __start_datetime = datetime.datetime.now()
    __alternative_datetime = datetime.datetime.now()
    
    @classmethod
    def now(cls):
        if cls.__in_time_machine_mode:
            time_difference = datetime.datetime.now() - cls.__start_datetime
            cls.__alternative_datetime = cls.__alternative_datetime + time_difference
            return cls.__alternative_datetime
        return datetime.datetime.now()
        
    @classmethod
    def start_time_machine_mode(cls):
        cls.__in_time_machine_mode = True

    @classmethod
    def stop_time_machine_mode(cls):
        cls.__in_time_machine_mode = False   

    @classmethod
    def in_time_machine_mode(cls):
        return cls.__in_time_machine_mode

    @classmethod
    def set_alternative_datetime(cls, in_datetime):
        cls.__start_datetime = datetime.datetime.now()
        cls.__alternative_datetime = in_datetime

