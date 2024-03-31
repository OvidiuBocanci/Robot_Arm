
import time


def nano_sleep(nanoseconds):
    start_time = time.perf_counter()
    end_time = start_time + nanoseconds/ 1e4
    # print(end_time)

    while time.perf_counter() < end_time:
        pass










