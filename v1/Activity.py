class Activity:
    """
    The Activity class stores information about an activity for a Camp.
    This information includes the type of activity, the start time, and the duration.
    It also includes some default values for the duration of certain types of activities.
    """

    class __ActivityType:
        """
        Default durations of different activities.
        TODO: Implement functionality for user-created activity types with their own default durations.
        """
        POOL = 45
        LOCKER = 15
        PLAYGROUND = 30

    def __init__(self, type, camp, start=None, duration=None):
        """
        An activity must be initialized with a type. The start time and duration can be set later.
        """
        raise NotImplementedError
    
    def start(self):
        """
        Return the start time of the Activity as a datetime object.
        """
        raise NotImplementedError
    
    def end(self):
        """
        Return the end time of the Activity as a datetime object.
        """
        raise NotImplementedError
    
    def set_time(self):
        """
        Set the start time of the Activity as a datetime object.
        """
        raise NotImplementedError
    
    def set_duration(self):
        """
        Set the duration of the Activity as a timedelta object.
        """
        raise NotImplementedError