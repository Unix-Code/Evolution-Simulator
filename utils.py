from functools import reduce
from math import sqrt, cos, sin


def euclid_distance(p0, p1):
    """ Returns euclidean distance between points p0 and p1
    p0 : (x, y)
    p1 : (x, y)
    """
    return sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def convert_polar_to_cartesian(r, theta):
    """Returns cartesian coordinates from polar coordinates
    r : magnitude/radius
    theta : angle (in Radians)
    """
    return (r * cos(theta)), (r * sin(theta))


def average(*nums):
    return reduce(lambda a, b: a + b, nums) / len(nums)


def max_by(objs, max_func):
    if objs:
        return reduce(lambda a, b: a if max_func(a) >= max_func(b) else b, objs, objs[0])
    else:
        return None


def min_by(objs, min_func):
    if objs:
        return reduce(lambda a, b: a if min_func(a) <= min_func(b) else b, objs, objs[0])
    else:
        return None
