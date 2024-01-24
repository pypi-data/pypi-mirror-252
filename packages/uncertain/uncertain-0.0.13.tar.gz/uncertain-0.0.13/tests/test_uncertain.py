import os
import pytest
import numpy as np
import sympy
import uncertain as uc
from uncertain import UncertainValue


# Variables for functions testing
a = uc.UncertainValue(5, 4, 6)
b = uc.UncertainValue(-2, -3, -1)
c = uc.UncertainValue(0, -2, 2)
d = np.array([1, 2, 3, 4, 5])
e = uc.UncertainValue(0.1, -.1, .3)


# @pytest.mark.timeout(10)
def test_definition():
    # Constant
    uc.UncertainValue(5)

    # Uniform
    uc.UncertainValue(0, -100, 100)
    uc.UncertainValue(0, -100, 100, 'uniform')
    uc.UncertainValue(0, -100, 100, 'uniform', None)

    # Normal distribution
    uc.UncertainValue(0, -100, +100, 'normal', [0, 1])
    a = [1, 2, 3, 4, 5]
    assert np.std(a) == pytest.approx(uc.UncertainValue(
        np.average(a), -np.inf, np.inf,
        'normal', [np.average(a), np.std(a)]).std, rel=1e-2)

    # Discrete
    def1 = uc.UncertainValue(1.15, None, None, 'discrete', [1, 1.1, 1.2, 1.3])
    def2 = uc.UncertainValue(1.15, None, None, 'discrete',
                             [[1, 0.2], [1.1, 0.3], [1.2, 0.4], [1.3, 0.1]])
    assert def1.lower_bound == 1
    assert def2.upper_bound == 1.3
    assert len(def1.samples) == 100000
    assert len(def2.samples) == 100000


# Mathematical operations
#  - UncertainValue with real numbers and other UncertainValues
#    from right and left side
def test_sum():
    a + 1
    1 + a
    a + sympy.core.numbers.Float(2)
    a + b
    with pytest.raises(TypeError):
        a + dict({1: 2})


def test_mul():
    2 * a
    a * 2
    a * sympy.core.numbers.Float(2)
    a * b
    with pytest.raises(TypeError):
        a * dict({1: 2})


def test_neg():
    -a


def test_sub():
    1 - b
    a - b
    sympy.core.numbers.Float(2) - b


def test_pow():
    a**2
    2**a
    a**a
    a**b
    try:
        b**a
    except ValueError:
        True


def test_truediv():
    2/a
    a/2
    a/b
    a/e


def test_sin():
    a = np.sin(UncertainValue(1.5, 1, 2, n_samples=2e4))
    assert a.upper_bound == 1.
    assert a.n_samples == 2e4

    b = np.sin(UncertainValue(-5, -8, -1))
    assert b.lower_bound == -1.
    assert b.upper_bound == 1.

    c = np.sin(UncertainValue(5/2*np.pi, 2*np.pi, 3*np.pi))
    assert c.upper_bound == 1.

    d = np.sin(UncertainValue(7/2*np.pi, 3*np.pi, 4*np.pi))
    assert d.lower_bound == -1.


def test_cos():
    a = np.cos(UncertainValue(3, 2.5, 3.5, n_samples=5e4))
    assert a.lower_bound == -1.

    b = np.cos(UncertainValue(-5, -8, -1))
    assert b.lower_bound == -1.
    assert b.upper_bound == 1.

    c = np.cos(UncertainValue(2*np.pi, 3/2*np.pi, 5/2*np.pi))
    assert c.upper_bound == 1.

    d = np.cos(UncertainValue(3*np.pi, 5/2*np.pi, 7/2*np.pi))
    assert d.lower_bound == -1.


def test_tan():
    a = np.tan(UncertainValue(0, -1.5, 1.5))
    assert a.nominal_value == 0
    assert a.lower_bound != -np.inf
    assert a.upper_bound != np.inf

    b = np.tan(UncertainValue(-5, -8, -1))
    assert b.lower_bound == -np.inf
    assert b.upper_bound == np.inf

    c = np.tan(UncertainValue(3.7, 3.5, 5))
    assert c.lower_bound == -np.inf
    assert c.upper_bound == np.inf


# Percentile
def test_percentile():
    assert a.percentile(25) == pytest.approx(4.5, rel=1e-2)


# Description
def test_description():
    a.describe()


# Plots
def test_plots():
    fname = 'testfile.png'
    a.plot_distribution(save=True, fname=fname)
    a.plot_distribution(save=True, fname=fname, label='X')
    a.plot_distribution(plot_type='cdf', save=True, fname=fname)
    with pytest.raises(ValueError):
        a.plot_distribution(plot_type='dakdgaskdjgajd')
    os.remove(fname)


def test_probability_in_interval():
    assert pytest.approx(uc.probability_in_interval(
        a, [-np.inf, 5]), rel=1e-2) == 0.5


# Generation from data
def test_from_data():
    e = uc.from_data(d)
    assert pytest.approx(e.mean, rel=1e-2) == 3.
    assert pytest.approx(e.std, rel=1e-2) == np.std(d)


# Samples
def test_constant():
    b = UncertainValue(1, n_samples=10)
    assert b.n_samples == 10
    assert (b.samples == np.array(10 * [1])).all


def test_samples():
    n_samples = 2e4
    a = UncertainValue(2, 1, 3, n_samples=n_samples)

    assert (-a).n_samples == n_samples
    assert (a + 2).n_samples == n_samples
    assert (2 + a).n_samples == n_samples
    assert (a - 2).n_samples == n_samples
    assert (2 - a).n_samples == n_samples
    assert (2 * a).n_samples == n_samples
    assert (a * 2).n_samples == n_samples
    assert (a / 2).n_samples == n_samples
    assert (2 / a).n_samples == n_samples
    assert (a**2).n_samples == n_samples
    assert (2**a).n_samples == n_samples
