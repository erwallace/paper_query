from paper_query.utils import random_string


def test_random_string():
    assert len(random_string()) == 6
    assert len(random_string(10)) == 10
    assert random_string() != random_string()
