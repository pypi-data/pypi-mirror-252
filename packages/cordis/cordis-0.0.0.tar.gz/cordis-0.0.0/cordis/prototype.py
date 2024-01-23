from collections import deque
from functools import reduce

PROTOTYPE = '__prototype__'


class Prototyped(type):
    __prototype__ = {}

    def __init_subclass__(cls, **kwargs):
        print('init subclass', cls, kwargs)

    def __call__(self, *args, **kwargs):
        getattr(self, PROTOTYPE).update(vars(self))
        self.__init__(self, *args, **kwargs)
        return self

    def __new__(cls, name, bases, attrs):
        prototypes = deque()

        bases = (cls,) + bases

        for base in bases:
            prototypes.append(getattr(base, '__prototype__', {}))

        attrs[PROTOTYPE] = reduce(lambda x, y: (x.update(y), x)[1], prototypes, {})
        return super().__new__(cls, name, bases, attrs)
