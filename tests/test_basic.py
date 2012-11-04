from classes.basic import make_class, get, set_, del_, new

from nose.tools import eq_, ok_, raises
from mock import Mock


def test_class_dont_require_attributes():
    TestClass = make_class('TestClass')
    instance = new(TestClass)


def test_class_instances_have_a_name():
    OtherTestClass = make_class('OtherTestClass')
    eq_(OtherTestClass['__name__'], 'OtherTestClass')


def test_init_is_called_upon_new():
    initializer = Mock()

    TestClass = make_class('TestClass', {
        '__init__': initializer
    })

    instance = new(TestClass)

    initializer.assert_called_once_with(instance)


def test_init_is_passed_arguments():
    initializer = Mock()

    TestClass = make_class('TestClass', {
        '__init__': initializer
    })

    instance = new(TestClass, 1, 2, a='b')

    initializer.assert_called_once_with(instance, 1, 2, a='b')


def test_instances_can_set_and_get_attributes():
    TestClass = make_class('TestClass', {
        '__init__': lambda self: set_(self, 'val', 1)
    })

    instance = new(TestClass)

    eq_(get(instance, 'val'), 1)


def test_attributes_can_exist_on_the_class():
    TestClass = make_class('TestClass', {
        'x': 1
    })

    instance = new(TestClass)

    eq_(get(instance, 'x'), 1)


def test_setting_an_attribute_shadows_the_class_attribute():
    TestClass = make_class('TestClass', {
        'x': 1
    })

    instance = new(TestClass)

    set_(instance, 'x', 2)
    eq_(get(instance, 'x'), 2)


@raises(AttributeError)
def test_missing_attributes_raise_attribute_error():
    TestClass = make_class('TestClass')

    instance = new(TestClass)

    get(instance, 'missing_value')


def test_methods_receive_the_instance_as_the_first_param():
    method = Mock()
    TestClass = make_class('TestClass', {
        'method': method
    })

    instance = new(TestClass,)
    get(instance, 'method')(1, 2)

    method.assert_called_once_with(instance, 1, 2)


def test_setting_an_instance_callable_does_not_receive_the_instance():
    method = Mock()
    TestClass = make_class('TestClass')

    instance = new(TestClass,)
    set_(instance, 'method', method)
    get(instance, 'method')(1, 2)

    method.assert_called_once_with(1, 2)


@raises(AttributeError)
def test_can_delete_instance_attributes():
    TestClass = make_class('TestClass')

    instance = new(TestClass)
    set_(instance, 'x', 1)
    get(instance, 'x')

    del_(instance, 'x')
    get(instance, 'x')


@raises(AttributeError)
def test_cannot_delete_class_attributes():
    TestClass = make_class('TestClass', {
        'x': 1
    })

    instance = new(TestClass)

    del_(instance, 'x')
