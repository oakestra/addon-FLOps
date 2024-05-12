import time

from context import get_context


def call_B():
    get_context().start_new_time_frame("3")
    time.sleep(4)
    get_context().end_time_frame("3")
