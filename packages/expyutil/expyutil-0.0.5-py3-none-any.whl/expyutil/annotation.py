import warnings
import functools

def _warn(msg):
    warnings.simplefilter('always', DeprecationWarning)  # turn off filter
    warnings.warn(msg, category=DeprecationWarning, stacklevel=2)
    warnings.simplefilter('default', DeprecationWarning)  # reset filter

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        _warn("Call to deprecated function {}.".format(func.__name__))
        return func(*args, **kwargs)
    return new_func

def symbolMoved(new_location):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _warn("Call to moved function {}.\nnew location -> {}".format(func.__name__, new_location))
            return(func(*args, **kwargs))
        return wrapper
    return deco

# Examples

@symbolMoved("../hashlib")
def some_old_function(x, y):
    return x + y

class SomeClass:
    @deprecated
    def some_old_method(self, x, y):
        return x + y
    
if __name__ == '__main__':
    some_old_function(1,2)