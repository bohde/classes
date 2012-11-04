from operator import itemgetter
from classes.basic import make_class, get, set_, del_, new

from nose.tools import eq_, ok_, raises
from mock import Mock

# These examples are taken from the Python docs on MRO

O = make_class('O')
A = make_class('A', bases=(O,))
B = make_class('B', bases=(O,))
C = make_class('C', bases=(O,))
D = make_class('D', bases=(O,))
E = make_class('E', bases=(O,))

K1 = make_class('K1', bases=(A,B,C))
K2 = make_class('K2', bases=(D,B,E))
K3 = make_class('K3', bases=(D,A))

Z = make_class('Z', bases=(K1, K2, K3))


def check_linearization(cls, expected):
    eq_(cls['mro'], expected)


def test_linearization_of_A():
    check_linearization(A, (A,O))


def test_linearization_of_B():
    check_linearization(B, (B, O))


def test_linearization_of_C():
    check_linearization(C, (C, O))


def test_linearization_of_D():
    check_linearization(D, (D, O))


def test_linearization_of_E():
    check_linearization(E, (E, O))

def test_linearization_of_K1():
    check_linearization(K1, (K1, A, B, C, O))


def test_linearization_of_K2():
    check_linearization(K2, (K2, D, B, E, O))


def test_linearization_of_K3():
    check_linearization(K3, (K3, D, A, O))


def test_linearization_of_Z():
    check_linearization(Z, (Z, K1, K2, K3, D, A, B, C, E, O))
