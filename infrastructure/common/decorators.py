import time


def time_perf(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Time taken to execute {func.__name__} is {end-start}")
        return result

    return wrapper
