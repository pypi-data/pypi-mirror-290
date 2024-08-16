import time
from contextlib import contextmanager

@contextmanager
def timer_ctx():
    st = time.time()
    yield
    ed = time.time()
    print(ed-st)

def timer_deco(func):
    def warpper(*args, **kwargs):
        st = time.time()
        func(*args, **kwargs)
        ed = time.time()
        print(func, round(ed-st, 5))
    return warpper



if __name__ == '__main__':
    pass
