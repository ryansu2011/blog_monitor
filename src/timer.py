import time


class Timer:
    """A timer for periodical callback!"""

    _sec_per_min = 60
    _sec_per_hour = 3600
    _hour_per_day = 24

    def __init__(self, notification_hours, callback):
        """
        :param notification_hours: list of integer between 0-23
        :param callback: call back function with caller id as input parameter
        """
        self._stime_list = []
        self._call_id = 0
        for hour in sorted(notification_hours):
            self._stime_list.append(Timer._get_stime(hour, 0, 0))
        self._callback_function = callback

    def start_counter(self):
        while True:
            sec = self._get_seconds_to_next_callback()
            print("Sleep {} seconds for the next callback!".format(sec))
            time.sleep(sec)
            self._call_id += 1
            self._callback_function(self._call_id)

    def _get_seconds_to_next_callback(self):
        stime_now = Timer._get_stime_now()
        for stime_target in self._stime_list:
            if stime_target > stime_now + Timer._sec_per_min:
                return stime_target - stime_now
        return self._stime_list[0] + Timer._hour_per_day * Timer._sec_per_hour - stime_now

    @staticmethod
    def _get_stime_now():
        cur = time.gmtime()
        return Timer._get_stime(cur.tm_hour, cur.tm_min, cur.tm_sec)

    @staticmethod
    def _get_stime(hour, minute, second):
        return second + minute * Timer._sec_per_min + hour * Timer._sec_per_min

