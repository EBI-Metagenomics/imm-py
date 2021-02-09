from collections.abc import Iterable
from math import isclose
from typing import SupportsFloat, Union


def assert_allclose(
    actual: Union[SupportsFloat, Iterable[SupportsFloat]],
    desired: Union[SupportsFloat, Iterable[SupportsFloat]],
    rtol: SupportsFloat = 1e-07,
    atol: SupportsFloat = 0,
):
    if isinstance(actual, Iterable) and isinstance(desired, Iterable):
        actual_list = list(actual)
        desired_list = list(desired)
        assert len(actual_list) == len(desired_list)
        for a, b in zip(actual_list, desired_list):
            assert isclose(a, b, rel_tol=rtol, abs_tol=atol)
    else:
        assert isinstance(actual, SupportsFloat)
        assert isinstance(desired, SupportsFloat)
        assert isclose(actual, desired, rel_tol=rtol, abs_tol=atol)
