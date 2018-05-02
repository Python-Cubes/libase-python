#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   smart.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

import functools


def smart_decorator(decorator):
    '''
        Smart decorator for decorator
    '''

    @functools.wraps(decorator)
    def decorator_proxy(func=None, **kwargs):
        '''
            Decorator proxy
        '''

        if func is not None:
            return decorator(func=func, **kwargs)

        @functools.wraps(decorator)
        def _decorator_proxy(func=None, **_kwargs):
            return decorator_proxy(func=func, **dict(kwargs, **_kwargs))

        return _decorator_proxy

    return decorator_proxy
