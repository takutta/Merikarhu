import pytest
from datetime import datetime, time
from luokat import Lapsi
from test_data import lapsi_data


@pytest.fixture
def lapset():
    return [Lapsi(**data) for data in lapsi_data]


@pytest.mark.parametrize(
    "lapsi_index, paiva, expected",
    [
        (0, 0, 4),
        (0, 1, 4),
        (0, 2, 8),
        (0, 3, 0),
        (0, 4, 2),
        (0, 5, 0),
        (0, 6, 0),
        (1, 0, 0),
    ],
)
def test_lapsi_aika_lkm(lapset, lapsi_index, paiva, expected):
    assert lapset[lapsi_index].aika_lkm(paiva) == expected


@pytest.mark.parametrize(
    "lapsi_index, paiva, expected",
    [
        (0, 0, [[time(9, 0), time(12, 0)], [time(13, 0), time(15, 0)]]),
        (0, 1, [[time(9, 0), time(11, 0)], [time(12, 0), time(14, 0)]]),
        (
            0,
            2,
            [
                [time(2, 0), time(4, 0), time(6, 0), time(12, 0)],
                [time(3, 0), time(6, 0), time(8, 0), time(16, 0)],
            ],
        ),
        (0, 3, []),
        (0, 4, [[time(11, 0)], [time(14, 0)]]),
        (0, 5, []),
        (0, 6, []),
    ],
)
def test_lapsi_lasna(lapset, lapsi_index, paiva, expected):
    assert lapset[lapsi_index].lasna(paiva) == expected


@pytest.mark.parametrize(
    "lapsi_index, paiva, expected",
    [
        (0, 0, [time(9, 0), time(12, 0), time(13, 0), time(15, 0)]),
        (0, 1, [time(9, 0), time(11, 0), time(12, 0), time(14, 0)]),
        (
            0,
            2,
            [
                time(2, 0),
                time(3, 0),
                time(4, 0),
                time(6, 0),
                time(8, 0),
                time(12, 0),
                time(16, 0),
            ],
        ),
        (0, 3, []),
        (0, 4, [time(11, 0), time(14, 0)]),
        (0, 5, []),
        (0, 6, []),
    ],
)
def test_lapsi_uniikit(lapset, lapsi_index, paiva, expected):
    assert lapset[lapsi_index].uniikit(paiva) == expected


@pytest.mark.parametrize(
    "lapsi_index, pvm, expected",
    [
        (0, datetime(2023, 1, 1), 1),
        (1, datetime.now(), 4),  # jos ei syntymäaikaa, lapsesta tulee 4v
        (2, datetime(2023, 1, 1), -1),  # syntymäaika tulevaisuudessa
        (3, datetime(2023, 1, 1), 0),
    ],
)
def test_lapsi_ika(lapset, lapsi_index, pvm, expected):
    assert lapset[lapsi_index].ika(pvm) == expected


@pytest.mark.parametrize(
    "lapsi_index, pvm, expected",
    [
        (0, datetime(2023, 1, 1), False),
        (1, datetime.now(), True),  # jos ei syntymäaikaa, lapsesta tulee 4v
        (2, datetime(2023, 1, 1), False),  # syntymäaika tulevaisuudessa
        (3, datetime(2023, 1, 1), False),
    ],
)
def test_lapsi_iso(lapset, lapsi_index, pvm, expected):
    assert lapset[lapsi_index].iso(pvm) == expected


@pytest.mark.parametrize(
    "lapsi_index, pvm, expected",
    [
        (0, datetime(2023, 1, 1), 1 / 4),
        (1, datetime.now(), 1 / 7),  # jos ei syntymäaikaa, lapsesta tulee 4v
        (2, datetime(2023, 1, 1), 1 / 4),  # syntymäaika tulevaisuudessa
        (3, datetime(2023, 1, 1), 1 / 4),
    ],
)
def test_lapsi_kerroin(lapset, lapsi_index, pvm, expected):
    assert lapset[lapsi_index].kerroin(pvm) == expected
