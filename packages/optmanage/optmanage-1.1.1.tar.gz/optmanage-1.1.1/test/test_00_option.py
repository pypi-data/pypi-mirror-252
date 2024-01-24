# pylint: disable = missing-docstring

from __future__ import annotations
from collections.abc import Sequence

import pytest
from optmanage.manager import OptionManager

from optmanage.option import Option

def test_option_attr_1() -> None:
    opt = Option(Sequence[float], [1.5, 2.])
    assert opt.default == [1.5, 2.]
    assert opt.type == Sequence[float]
    assert opt.validator is None
    with pytest.raises(AttributeError):
        opt.name # pylint: disable = pointless-statement
    with pytest.raises(AttributeError):
        opt.owner # pylint: disable = pointless-statement

def test_option_validation_1() -> None:
    opt = Option(Sequence[float], [1.5, 2.])
    opt.validate([1e-8])
    with pytest.raises(TypeError):
        opt.validate(1e-8) # type: ignore
    with pytest.raises(TypeError):
        Option(Sequence[float], 1e-8)

def test_option_attr_2() -> None:
    validator = lambda x: x>= 0
    opt = Option(float, 1e8, validator)
    assert opt.validator == validator

def test_option_validation_2() -> None:
    opt = Option(float, 1e8, lambda x: x>= 0)
    with pytest.raises(ValueError):
        opt.validate(-1.5)
    with pytest.raises(ValueError):
        Option(float, -1.5, lambda x: x>= 0)

def test_option_assignment() -> None:
    class MyOptions(OptionManager):
        validate = Option(bool, True)
    opt = MyOptions.validate
    assert opt.name == "validate"
    assert opt.owner == MyOptions
