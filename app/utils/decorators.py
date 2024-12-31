import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"\nFunction {func.__name__} took {elapsed_time:.6f}s\n")
        return result
    return wrapper