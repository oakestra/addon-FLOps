import time

from B import call_B
from context import get_context, init_context
from icecream import ic

init_context()
get_context().start_new_time_frame("1")
time.sleep(3)
get_context().start_new_time_frame("2")
time.sleep(2)
get_context().end_time_frame("2")
call_B()
get_context().end_time_frame("1")

for name, timeframe in get_context().time_frames.items():
    ic(name, timeframe.get_duration(human_readable=True), timeframe)
