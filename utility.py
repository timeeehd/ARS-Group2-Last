import math


def calc_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def calc_angle(p1, p2):
    return math.atan(abs(p1[1] - p2[1]) / abs(p1[0] - p2[0]))
