import pytest
from datetime import datetime
from luokat import Tyontekija, Lapsi
from test_data import tyontekija_data, lapsi_data, ryhma_data


@pytest.fixture
def lapset():
    return [Lapsi(**data) for data in lapsi_data]


@pytest.fixture
def tyontekija():
    return [Tyontekija(**data) for data in tyontekija_data]


@pytest.fixture
def ryhmat():
    return [Ryhma(**data) for data in ryhma_data]


# @pytest.mark.parametrize(
#     "lapsi_index, paiva, expected",
#     [(0, 0, 4), (0, 1, 4), (0, 2, 8), (0, 3, 0), (0, 4, 2), (0, 5, 0), (0, 6, 0)],
# )
# def test_lapsi_aika_lkm(lapset, lapsi_index, paiva, expected):
#     assert lapset[lapsi_index].aika_lkm(paiva) == expected


# # Testit Tyontekija-luokalle
# def test_lapsi_aika_lkm(lapset):
#     assert lapset[0].aika_lkm(0) == 2


# def test_tyontekija_valid_time():
#     tyontekija = Tyontekija(**tyontekija_data)
#     assert tyontekija.valid_time(
#         "9.00"
#     )  # Tarkistetaan, että valid_time palauttaa True, kun syöte on validi aika.


# def test_tyontekija_lasna():
#     tyontekija = Tyontekija(**tyontekija_data)
#     datetime_values = tyontekija.lasna("paiva1")
#     assert (
#         datetime_values[0][0] == datetime.strptime("9.00", "%H.%M").time()
#     )  # Tarkistetaan, että palautettu aika on oikea.


# # Testit Lapsi-luokalle
# def test_lapsi_lasna():
#     lapsi = Lapsi(**lapsi_data)
#     datetime_values = lapsi.lasna("paiva1")
#     assert (
#         datetime_values[0][0] == datetime.strptime("9.00", "%H.%M").time()
#     )  # Tarkistetaan, että palautettu aika on oikea.


# def test_lapsi_aika_lkm():
#     lapsi = Lapsi(**lapsi_data)
#     assert (
#         lapsi.aika_lkm("paiva1") == 4
#     )  # Tarkistetaan, että aika_lkm palauttaa oikean lukumäärän.


# def test_lapsi_ika():
#     lapsi = Lapsi(**lapsi_data)
#     assert (
#         lapsi.ika(datetime.now()) == 2
#     )  # Tarkistetaan, että ika palauttaa oikean iän.
