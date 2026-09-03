from main import largest


def test_positive_numbers():
    assert largest([1, 5, 3, 9, 2]) == 9


def test_negative_numbers():
    assert largest([-10, -3, -7]) == -3


def test_single_element():
    assert largest([42]) == 42