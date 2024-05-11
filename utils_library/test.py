from flops_utils.timer import Timer
from icecream import ic

timer = Timer()
full_process = timer.start_new_time_frame("full_process")
a = timer.start_new_time_frame("aaa")
# Code A
a.end_time_frame()

b = timer.start_new_time_frame("bbb")
# Code B
b.end_time_frame()

c = timer.start_new_time_frame("ccc")
# Code C
c.end_time_frame()
z = timer.get_time_frame("full_process")
z.end_time_frame()
ic(z.get_duration(human_readable=True))
# ic(a.get_human_readable_duration())
# ic(b.get_human_readable_duration())

# ic(timer.get_time_frame("aaa").get_human_readable_duration())
