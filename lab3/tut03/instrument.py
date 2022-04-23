from functools import wraps
import sys

def instrument(f):
    """Show call entry/exits on stderr

    Wrapper to instrument a function to show the
    call entry and exit from that function. Can
    customize view with instrument flags.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        arg_str = ', '.join(str(a) for a in args)
        if instrument.TRIM_ARGS is not None and len(arg_str) > instrument.TRIM_ARGS:
            arg_str = arg_str[:instrument.TRIM_ARGS] + " ..."
        if instrument.SHOW_CALL:
            sys.stderr.write("   "*wrapper._depth + "call to " + f.__name__ + ": " + arg_str + "\n")
        wrapper._count += 1
        wrapper._depth += 1
        wrapper._max_depth = max(wrapper._depth, wrapper._max_depth)
        result = f(*args, **kwargs)
        wrapper._depth -= 1
        res_str = str(result)
        if instrument.TRIM_RET is not None and len(res_str) > instrument.TRIM_RET:
            res_str = res_str[:instrument.TRIM_RET] + " ..."
        if instrument.SHOW_RET:
            sys.stderr.write("   "*wrapper._depth + f.__name__ + " returns: " +  res_str + "\n")
        return result
    wrapper._count = 0
    wrapper._depth = 0
    wrapper._max_depth = 0
    return wrapper

instrument.SHOW_CALL = True
instrument.SHOW_RET = True
instrument.TRIM_ARGS = 55  #None if no trimming
instrument.TRIM_RET = 60   #None if no trimming
