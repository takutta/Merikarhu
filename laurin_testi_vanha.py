from openpyxl import load_workbook
import pandas as pd
import warnings


def load_data(path: str, sheet: list):
    """Load data from an Excel file."""
    warnings.simplefilter(action="ignore", category=UserWarning)
    return pd.read_excel(path, sheet)


excel_valilehdet = ["Kiertotunnus", "Vuorokoodit", "Omakierto"]
excel = load_data("tapiolan_kiertopohjat_tunnukset.xlsm", excel_valilehdet)


def muokkaa_vuorokoodit(df, b: bool):
    # Jos B-lista
    if b:
        df = df.drop(columns=df.columns[0:8])
        print(df)
    # ei rivejä tyhjän jälkeen sarakkeessa 0, sarakkeet 0:7
    df = df.iloc[: df.iloc[:, 0].isna().idxmax(), 0:7]
    # poistetaan sarake 1 ja rivi 0
    df = df.drop(columns=[df.columns[1]]).drop(index=0)
    # nimetään sarakkeet
    df = df.rename(
        columns={
            df.columns[0]: "Koodi",
            df.columns[1]: "Alku",
            df.columns[2]: "Loppu",
            df.columns[3]: "Kesto",
            df.columns[4]: "Koko vuoro",
            df.columns[5]: "Tyyppi",
        }
    )
    return df


def muokkaa_kiertotunnus(df):
    df = df.iloc[: df.iloc[:, 0].isna().idxmax(), 0:23]
    df = df.rename(
        columns={
            df.columns[0]: "Kiertolista",
            df.columns[1]: "1ma",
            df.columns[2]: "1ti",
            df.columns[3]: "1ke",
            df.columns[4]: "1to",
            df.columns[5]: "1pe",
            df.columns[6]: "1la",
            df.columns[7]: "1su",
            df.columns[8]: "2ma",
            df.columns[9]: "2ti",
            df.columns[10]: "2ke",
            df.columns[11]: "2to",
            df.columns[12]: "2pe",
            df.columns[13]: "2la",
            df.columns[14]: "2su",
            df.columns[15]: "3ma",
            df.columns[16]: "3ti",
            df.columns[17]: "3ke",
            df.columns[18]: "3to",
            df.columns[19]: "3pe",
            df.columns[20]: "3la",
            df.columns[21]: "3su",
            df.columns[22]: "Ryhmä",
        }
    )
    return df


def muokkaa_omakierto(df):
    df = df.drop(columns=[df.columns[1:3]]).drop(index=0)

    df = df.iloc[: df.iloc[:, 0].isna().idxmax(), 0:23]


for sheet_name, df in excel.items():
    if sheet_name == "Vuorokoodit":
        vuorokoodit = muokkaa_vuorokoodit(df, False)
        # Katsotaan onko 2. vuorokoodi-listaa
        # if not pd.isna(df.iloc[0, 8]):
        #     vuorokoodit_B = muokkaa_vuorokoodit(df, True)

    elif sheet_name == "Kiertotunnus":
        kiertotunnus = muokkaa_kiertotunnus(df)
    elif sheet_name == "Omakierto":
        omakierto = muokkaa_omakierto(df)

    # elif sheet_name == "Titania":
