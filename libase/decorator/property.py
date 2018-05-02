#!/usr/bin/env python
# -*- encoding=utf8 -*-

'''
FileName:   property.py
Author:     Fasion Chan
@contact:   fasionchan@gmail.com
@version:   $Id$

Description:

Changelog:

'''

from .smart import (
    smart_decorator,
)


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel

    def getter(self, getter):
        return self.__class__(
            fget=getter,
            fset=self.fset,
            fdel=self.fdel,
        )

    def setter(self, setter):
        return self.__class__(
            fget=self.fget,
            fset=setter,
            fdel=self.fdel,
        )

    def deleter(self, deleter):
        return self.__class__(
            fget=self.fget,
            fset=self.fset,
            fdel=deleter,
        )

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        return self.fget.__get__(obj, cls)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError('can not set attribute')
        cls = type(obj)
        return self.fset.__get__(obj, cls)(value)

    def __delete__(self, obj):
        if not self.fset:
            raise AttributeError('can not delete attribute')
        cls = type(obj)
        return self.fdel.__get__(obj, cls)()


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)


@smart_decorator
def cached_property(func, attr_name=None, property_func=property,
        with_setter=False, with_deleter=False, no_such=[]):

    if not attr_name:
        func_name = (
            getattr(func, '__name__', None) or
            getattr(func, 'func_name', None)
        )

        attr_name = '_cp_' + func_name

    @property_func
    def proxy(bind):

        value = getattr(bind, attr_name, no_such)
        if value is not no_such:
            return value

        value = func(bind)

        setattr(bind, attr_name, value)

        return value

    if with_setter:

        @proxy.setter
        def proxy(bind, value):

            setattr(bind, attr_name, value)

    if with_deleter:

        @proxy.deleter
        def proxy(bind):

            value = getattr(bind, attr_name, no_such)
            if value is not no_such:
                delattr(bind, attr_name)

    return proxy
