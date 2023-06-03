import pandas as pd
import numpy as np
from re import match

# Pandas asetuksia


def titania_import(tiedoston_nimi):
    pd.set_option("display.max_columns", 7)  # Näytä kaikki sarakkeet
    pd.set_option("display.max_rows", 70)  # Näytä kaikki rivit
    pd.set_option("display.width", None)  # Leveys mukautuu automaattisesti
    pd.set_option("display.unicode.ambiguous_as_wide", True)

    # Luetaan tiedosto (header-rivi 2)
    df = pd.read_csv(
        tiedoston_nimi, sep="\t", encoding="latin1", header=None, on_bad_lines="warn"
    )

    def remove_extra_spaces(cell):
        if pd.notnull(cell) and isinstance(cell, str):
            return " ".join(cell.split())
        else:
            return cell

    # Käytä applymap-funktiota poistamaan ylimääräiset välilyönnit jokaisesta solusta
    df = df.applymap(remove_extra_spaces)

    df.columns = df.iloc[3]  # Valitse 3. rivi (indeksi 2) ja aseta se headeriksi
    df = df.iloc[5:]  # Poista 3 ensimmäistä riviä

    # Poistetaan kaikki # merkit
    df = df.replace("#", "", regex=True)

    # Poista 2 viimeistä saraketta
    df.drop(df.columns[-2:], axis=1, inplace=True)

    # Poistetaan jos solun sisältö pelkkä piste
    def remove_dots(cell):
        if isinstance(cell, str) and cell != ".":
            return cell.replace(".", "")
        else:
            return cell

    df = df.applymap(remove_dots)

    # Poistetaan tyhjät sarakkeet ja rivit
    df.dropna(axis=1, how="all", inplace=True)
    df.dropna(axis=0, how="all", inplace=True)

    # Nimetään sarake ja täytetään sarake nimillä
    df.columns = [
        "nimi",
        "ma",
        "ti",
        "ke",
        "to",
        "pe",
        "la",
        "su",
        "ma2",
        "ti2",
        "ke2",
        "to2",
        "pe2",
        "la2",
        "su2",
        "ma3",
        "ti3",
        "ke3",
        "to3",
        "pe3",
        "la3",
        "su3",
    ]
    df["nimi"] = df["nimi"].apply(lambda x: x if x.strip() else np.nan)
    df["nimi"].fillna(method="ffill", inplace=True)

    # Jos ei työaikoja rivillä, poista koko rivi
    df.dropna(subset=df.columns[1:], how="all", inplace=True)
    df = df[df["nimi"].str.strip() != "#"]

    df.to_csv("titania_output.txt", sep=";", index=False)


def hae_kutsumanimi(nimi):
    sanat = nimi.split()
    if len(sanat) == 1:
        return sanat[0]
    toinen = sanat[1]
    ensimmainen = sanat[0]
    kutsumanimi = toinen + " " + ensimmainen[0]
    return kutsumanimi


# def csv_fix(tiedosto):
#     tyontekijat = []
#     with open("titania_output.txt", "r", encoding="utf-8") as t:
#         teksti = ""
#         for rivi in t:
#             rivi = rivi.strip()
#             vastaavuus = match(r"^[^0-9:]*;+ *$", rivi)
#             if not vastaavuus and rivi != "":
#                 teksti += rivi.replace("\\", "S") + "\n"
#     for rivi in teksti.splitlines():
#         csv = rivi.split(";")
#         nimi = csv[0]
#         found = any(nimi == dict.get("kokonimi") for dict in tyontekijat)
#         if not found and nimi != "nimi":
#             tyontekija = {}
#             tyontekija["kokonimi"] = nimi
#             tyontekija["kutsumanimi"] = hae_kutsumanimi(nimi)
#             for i, tyoaika in enumerate(csv[1:]):
#                 tyoaika = tyoaika.strip()
#                 if tyoaika != "" and tyoaika != ".":
#                     if "tyoajat" not in tyontekija:
#                         tyontekija["tyoajat"] = {}
#                     if i + 1 not in tyontekija["tyoajat"]:
#                         tyontekija["tyoajat"][i + 1] = []
#                     tyontekija["tyoajat"][i + 1].append(tyoaika)

#             tyontekijat.append(tyontekija)
#         elif found and nimi != "nimi":
#             for tyontekija in tyontekijat:
#                 if tyontekija["kokonimi"] == csv[0]:
#                     for i, tyoaika in enumerate(csv[1:]):
#                         tyoaika = tyoaika.strip()
#                         if tyoaika != "" and tyoaika != ".":
#                             if "tyoajat" not in tyontekija:
#                                 tyontekija["tyoajat"] = {}
#                             if i + 1 not in tyontekija["tyoajat"]:
#                                 tyontekija["tyoajat"][i + 1] = []
#                             tyontekija["tyoajat"][i + 1].append(tyoaika)
#     return tyontekijat


def lue_tiedosto(tiedosto):
    with open(tiedosto, "r", encoding="utf-8") as t:
        return [rivi.strip() for rivi in t]


def siisti_rivit(rivit):
    return [
        rivi.replace("\\", "S")
        for rivi in rivit
        if match(r"^[^0-9:]*;+ *$", rivi) is None and rivi != ""
    ]


def luo_tyontekija(csv):
    tyontekija = {
        "kokonimi": csv[0],
        "kutsumanimi": hae_kutsumanimi(csv[0]),
        "tyoajat": luo_tyoajat(csv[1:]),
    }
    return tyontekija


def luo_tyoajat(tyoajat):
    return {
        i + 1: [tyoaika.strip()]
        for i, tyoaika in enumerate(tyoajat)
        if tyoaika.strip() != "" and tyoaika.strip() != "."
    }


def lisaa_tyoajat(tyontekija, csv):
    for i, tyoaika in enumerate(csv[1:]):
        tyoaika = tyoaika.strip()
        if tyoaika != "" and tyoaika != ".":
            if i + 1 not in tyontekija["tyoajat"]:
                tyontekija["tyoajat"][i + 1] = []
            tyontekija["tyoajat"][i + 1].append(tyoaika)
    return tyontekija


def csv_fix(tiedosto):
    rivit = lue_tiedosto(tiedosto)
    siistityt_rivit = siisti_rivit(rivit)
    tyontekijat = []
    for rivi in siistityt_rivit:
        csv = rivi.split(";")
        nimi = csv[0]
        if nimi == "nimi":
            continue
        tyontekija = next(
            (
                tyontekija
                for tyontekija in tyontekijat
                if tyontekija["kokonimi"] == nimi
            ),
            None,
        )
        if tyontekija is None:
            tyontekija = luo_tyontekija(csv)
            tyontekijat.append(tyontekija)
        else:
            tyontekija = lisaa_tyoajat(tyontekija, csv)
    return tyontekijat


if __name__ == "__main__":
    titania_import("TPK12063.txt")
    tyontekijat = csv_fix("titania_output.txt")
    print(tyontekijat)
