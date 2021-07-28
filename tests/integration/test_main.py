import pytest

from src import main

@pytest.mark.parametrize("ttask", [(20), (-1), (0)])
def test_if_invalid_ttask_value_was_raised(ttask):
    with pytest.raises(main.InvalidTtaskValue):
        main.main([ttask, 5, 1])

@pytest.mark.parametrize("umax", [(20), (-1), (0)])
def test_if_invalid_umax_value_was_raised_with_big_value(umax):
    with pytest.raises(main.InvalidUmaxValue):
        main.main([5, umax, 1])

@pytest.mark.parametrize("payload, result", [
    ([3, 2, 1], 3),
    ([3, 2, 1, 1], 4),
    ([4, 2, 1, 3, 0, 1, 0, 1], 15),
    ([3, 3, 1, 0, 3, 0, 1], 10)
])
def test_if_the_costs_values_was_equals_expected(payload, result):
    assert main.main(payload) == result

