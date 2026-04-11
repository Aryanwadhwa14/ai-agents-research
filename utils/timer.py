import time
from contextlib import contextmanager

@contextmanager
def Timer(name="Task"):
    start = time.time()
    yield
    end = time.time()
    elapsed = end - start
    # print(f"[{name}] took {elapsed:.4f} seconds")

def get_latency(func, *args, **kwargs):
    start = time.time()
    result = func(*args, **kwargs)
    latency = time.time() - start
    return result, latency
