import src.timer as timer
import time


def callback(call_id):
    print(call_id)
    print("Callback at: {}".format(time.ctime()))


timer.Timer._sec_per_min = 2
timer.Timer._sec_per_hour = 5
tm1 = timer.Timer([1, 2, 3], callback)
tm1._stime_list = []
stime_now = timer.Timer._get_stime_now()
for i in range(4):
    tm1._stime_list.append(stime_now - 5 + i * 5)
tm1.start_counter()

