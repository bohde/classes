from collections import Callable
from functools import partial
from .mro import merge_mro

def make_class(name, bases=tuple(), cls_dict=None):
    """
    Construct a class dictionary
    """
    cls = {
        '__name__': name,
        '__bases__': bases,
    }
    cls.update(cls_dict or {})

    base_mros = [[cls]] + [b['mro'] for b in bases]
    cls['mro'] = tuple(merge_mro(base_mros))
    return cls


def new(cls, *args, **kwargs):
    """
    Construct a new instance of the given class
    """
    instance = {
        '__class__': cls
    }

    init = cls.get('__init__', None)
    if init:
        init(instance, *args, **kwargs)

    return instance


def get(instance, attr_name):
    """
    Retrieve the instance attribute, binding it if it is a method.
    """
    if attr_name in instance:
        return instance[attr_name]

    for cls in instance['__class__']['mro']:
        if attr_name in cls:
            attr = cls[attr_name]

            if isinstance(attr, Callable):
                attr = partial(attr, instance)

            elif isinstance(attr, staticmethod):
                attr = attr.__func__

            elif isinstance(attr, classmethod):
                attr = partial(attr.__func__, cls)

            return attr

    raise AttributeError("'%s' instanceect has no attribute '%s'" %
                         (cls['__name__'], attr_name))


def set_(instance, attr_name, val):
    """
    Set the instance attribute to the value
    """
    instance[attr_name] = val


def del_(instance, attr_name):
    """
    Delete the instance attribute
    """
    if attr_name in instance:
        del instance[attr_name]
    raise AttributeError(attr_name)
