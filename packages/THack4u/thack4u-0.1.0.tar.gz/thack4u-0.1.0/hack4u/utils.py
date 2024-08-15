#!/usr/bin/env python3

from .courses import courses

def totalDuration():
    return sum(course.duration for course in courses)
