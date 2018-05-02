#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   smart_decorator.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import logging
import functools

from time import (
    sleep,
    time as get_cur_ts,
)

from libase.decorator.smart import (
    smart_decorator,
)


@smart_decorator
def log_expired_time(func, threshold=0.1):

    @functools.wraps(func)
    def func_proxy(*args, **kwargs):
        start_ts = get_cur_ts()
        r = func(*args, **kwargs)
        end_ts = get_cur_ts()

        expired_time = end_ts - start_ts
        if expired_time > threshold:
            logging.warn('call %s with %f seconds' % (
                func.__name__,
                expired_time,
            ))

        return r

    return func_proxy


@log_expired_time
def small_job(x=0.001):
    print('small job')
    sleep(x)


@log_expired_time(threshold=1)
def big_job(x=0.1):
    print('big job')
    sleep(x)

small_job()
small_job(0.5)

big_job()
big_job(2)
