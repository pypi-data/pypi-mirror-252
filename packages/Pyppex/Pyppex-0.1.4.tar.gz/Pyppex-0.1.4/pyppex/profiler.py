from typing import Callable, TextIO
from datetime import datetime as dt, timedelta as td
from functools import wraps
import tracemalloc as tm
import os, time



def profiler(path:TextIO, until:int=7):
    '''
    A decorator for profiling the execution time and memory usage of a function and logging the results to a CSV file.

    Args:
    -----
        - `path` (TextIO): A file object (opened in 'a' mode) to write the profiling results in CSV format.
        - `until` (int): The number of days to keep in the CSV file. Default is 7 days.

    Usage:
    ------
    >>> arg1 = 1
    >>> arg2 = {'base_info': {'video_name': 'test', 'FPS': 30}}
    >>> @profiler('path/to/file.csv')
    >>> def example_function(arg1, arg2):
    ...    # function implementation

    The decorator logs the following information to the CSV file:
        - `date` (str): The date in 'YYYY-MM-DD' format.
        - `time` (str): The time in 'HH:MM:SS.SSS' format.
        - `duration` (str): The duration of the function execution in seconds.
        - `function` (str): The name of the decorated function.
        - `argument` (str): The argument passed to the function.
        - `memory_MiB` (float): The memory usage of the function in MB (megabytes).
        - `process_id` (int): The process ID (PID) of the Python process running the function.
        - `file_name` (str): The name of the file executed for the function.

    Example CSV structure:
    ----------------------
        date       | time         | duration(s) | function | argument | memory(MB) | process_id
        ---------------------------------------------------------------------------------------
        2023-12-24 | 10:31:12.45  | 0.123       | func1    | test     | 0.823      | 12345     
        2024-01-02 | 10:32:25.678 | 12.345      | func2    | test     | 122.2      | 67890     
    '''
    def decorator(func:Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            t = dt.now()
            # Save video name from metadatat if exists, otherwise use the first argument
            try:
                arg = [i['base_info']['video_name'] for i in args if isinstance(i, dict)][0]
            except:
                arg = args[0] if args else None

            start = time.time()
            tm.start()
            result = func(*args, **kwargs)
            memory = round(tm.get_traced_memory()[1] / 1024**2, 4)
            tm.stop()
            end = time.time()
            pid = os.getpid()

            # Write to file
            delimeter = '|'
            header = delimeter.join(['date', 'time', 'duration(s)', 'function', 'argument', 'memory(MB)', 'process_id'])
            if os.path.exists(path):
                data = open(path, 'r').read().split('\n')[1:]
                data = list(filter(lambda x: False if x == '' else True, data))
                data =  '\n'.join(data[len(data) - len(list(filter(lambda x: False if dt.strptime(x.split(delimeter)[0], '%Y-%m-%d') < dt.now() - td(until) else True, data))):])

                with open(path, 'w', newline='') as file:
                    file.write(header + '\n' + data)
                    file.write('\n' + delimeter.join([t.strftime('%Y-%m-%d'), t.strftime('%H:%M:%S.%f')[:-3], str(round(end-start, 3)), func.__name__, str(arg), str(memory), str(pid)]))

            else:
                with open(path, 'w', newline='') as file:
                    file.write(header)
                    file.write('\n' + delimeter.join([t.strftime('%Y-%m-%d'), t.strftime('%H:%M:%S.%f')[:-3], str(round(end-start, 3)), func.__name__, str(arg), str(memory), str(pid)]))


            return result
        return wrapper
    return decorator