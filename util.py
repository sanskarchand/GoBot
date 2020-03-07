#!/usr/bin/env python


def is_valid_index(points_array_size, index):
    return index >= 0 and index < points_array_size * points_array_size

def is_left_edge(points_array_size, index):
    # e.g. 9x9, left edge = 0,9,18,..72
    # i.e. ind % 9 == 0
    return index % points_array_size == 0

def is_right_edge(points_array_size, index):
    # 8, 17, ...
    return  (index+1) % points_array_size == 0

def is_upper_edge(points_array_size, index):
    # 0...8
    return index in list(range(points_array_size))

def is_lower_edge(points_array_size, index):
    # 72...80
    s = points_array_size
    return index in list(range(s*(s-1), s*s))
