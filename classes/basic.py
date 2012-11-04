from functools import partial
from collections import Callable


def make_class(name, cls_dict=None):
    """
    Construct a class dictionary
    """
    cls = {
        '__name__': name,
    }
    cls.update(cls_dict or {})
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

    cls = instance['__class__']
    if attr_name in cls:
        attr = cls[attr_name]
        if isinstance(attr, Callable):
            attr = partial(attr, instance)
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
