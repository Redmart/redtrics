# -*- coding: utf-8 -*-

import functools


def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
    return wrapper
