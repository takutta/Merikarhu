import pytest
from datetime import time
from luokat import Tyontekija
from test_data import tyontekija_data


@pytest.fixture
def tyontekijat():
    return [Tyontekija(**data) for data in tyontekija_data]


@pytest.mark.parametrize(
    "tyontekija_index, paiva, expected",
    [
        (0, 0, 4),
        (0, 1, 4),
        (0, 2, 2),
        (0, 3, 0),
        (0, 4, 2),
        (0, 5, 4),
        (0, 6, 2),
        (0, 7, 0),
        (0, 8, 0),
    ],
)
def test_tyontekija_lasna_lkm(tyontekijat, tyontekija_index, paiva, expected):
    assert tyontekijat[tyontekija_index].lasna_lkm(paiva) == expected


@pytest.mark.parametrize(
    "tyontekija_index, paiva, expected",
    [
        (0, 0, [[time(9, 0), time(12, 0)], [time(13, 0), time(15, 0)]]),
        (0, 1, [[time(10, 0), time(12, 0)], [time(12, 0), time(14, 0)]]),
        (0, 2, [[time(11, 0)], [time(14, 0)]]),
        (0, 3, []),
        (0, 4, [[time(11, 0)], [time(14, 0)]]),
        (0, 5, [[time(10, 0), time(22, 59)], [time(12, 0), time(23, 59)]]),
        (0, 6, [[time(0, 0)], [time(12, 59)]]),
        (0, 7, []),
        (0, 8, []),
    ],
)
def test_tyontekija_lasna(tyontekijat, tyontekija_index, paiva, expected):
    assert tyontekijat[tyontekija_index].lasna(paiva) == expected


@pytest.mark.parametrize(
    "tyontekija_index, paiva, expected",
    [
        (0, 0, [time(9, 0), time(12, 0), time(13, 0), time(15, 0)]),
        (0, 1, [time(10, 0), time(12, 0), time(14, 0)]),
        (0, 2, [time(11, 0), time(14, 0)]),
        (0, 3, []),
        (0, 4, [time(11, 0), time(14, 0)]),
        (0, 5, [time(10, 0), time(12, 0), time(22, 59), time(23, 59)]),
        (0, 6, [time(0, 0), time(12, 59)]),
        (0, 7, []),
        (0, 8, []),
    ],
)
def test_tyontekija_uniikit(tyontekijat, tyontekija_index, paiva, expected):
    assert tyontekijat[tyontekija_index].uniikit(paiva) == expected
