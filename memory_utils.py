"""
Here we write a set of functions that help us access certain properties of the variables such as:
- its memory usage (size)
-

Check out this way of tracing each line's memory usage in python:

    # importing the library
    from memory_profiler import profile
    
    # instantiating the decorator
    @profile
    # code for which memory has to
    # be monitored
    def my_func():
        x = [x for x in range(0, 1000)]
        y = [y*100 for y in range(0, 1500)]
        del x
        return y
    
    if __name__ == '__main__':
        my_func()
"""
import sys


def sizeof_fmt(num, suffix='B'):
    ''' by Fred Cirera,  https://stackoverflow.com/a/1094933/1870254, modified'''
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)

def get_vars_size(vars=list(locals().items())):
    """
    return the size and name of the list of variables you give to the function.
    If you want to get the size of all variables in your python session, you have to pass
    this to the function as argument:
        list(locals().items())
    If you let it empty, it will default to the local variables within this script, not yours.
    """   
    print("listing the size of certain variables:")
    print("{} variables".format(len(vars)))
    for name, size in sorted(((name, sys.getsizeof(value)) for name, value in vars), key= lambda x: -x[1])[:30]:
        print("{:>30}: {:>8}".format(name, sizeof_fmt(size)))


 

