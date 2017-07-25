from os import chdir
from sys import path
from itertools import tee

# standard recipe from https://docs.python.org/3/library/itertools.html
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

# xverges at https://stackoverflow.com/questions/1432924/
def reset_working_directory():
    chdir(path[0])
