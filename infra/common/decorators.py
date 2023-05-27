import time


def time_perf(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"Time taken to execute {func.__name__} is {end-start}")
        return result

    return wrapper


def measure_fps(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = 1 / elapsed_time
        print(f"FPS: {fps}")
        return result

    return wrapper
