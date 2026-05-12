import time
import psutil
import threading
import numpy as np

FREE_RAM = []


def ram_per_second(stop_event=threading.Event()):
    FREE_RAM.clear()
    FREE_RAM.append(psutil.virtual_memory().free / 1024**3)  # initial usage
    while not stop_event.is_set():
        # what is ACTUALLY used up, not process dependent
        # NOTE: run this with as few active programs at a time.
        FREE_RAM.append(psutil.virtual_memory().free / 1024**3)
        time.sleep(1)


class RamMeasure(object):
    '''
    >>> with RamMeasure() as rm:
    ...     print(rm.used)
    '''

    def __init__(self):
        self._t = None
        self._stop_event = None
        self.used = -1

    def __enter__(self):
        self._stop_event = stop_event = threading.Event()
        self._t = t = threading.Thread(target=ram_per_second, kwargs=dict(stop_event=stop_event))
        t.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._stop_event.set()
        self._t.join(timeout=5)
        self.used = FREE_RAM[0] - np.quantile(FREE_RAM[1:], 0.25)


lst = list(range(1000))
with RamMeasure() as rm:
    then = time.time()
    while time.time() - then < 5:
        lst.extend(lst)  # exponential growth

print(f'used {rm.used:0.3f} GB')
del lst  # really important...
