from datetime import datetime, time, timedelta
from re import match


class Henkilo:
    def __init__(self, nimi: str, kutsumanimi: str, ryhma: str = "", ajat: dict = {}):
        self.nimi = nimi
        self.kutsumanimi = kutsumanimi
        self.ryhma = ryhma
        self.ajat = ajat or {}


class Tyontekija(Henkilo):
    def __init__(
        self,
        nimi: str,
        kutsumanimi: str,
        ryhma: str = "",
        ajat: dict = {},
        vastuullinen: bool = True,
    ):
        super().__init__(nimi, kutsumanimi, ryhma, ajat)
        self.vastuullinen = vastuullinen

    def lasna_lkm(self, paiva) -> int:
        lasna_ajat = []
        if paiva in self.ajat and self.ajat[paiva] and self.ajat[paiva] != "P":
            ajat = self.ajat[paiva]
            for tulo, meno in zip(ajat[0], ajat[1]):
                if not tulo.startswith(("K", "S")):
                    if self.oikea_aika(tulo):
                        lasna_ajat.append(tulo)
                    if self.oikea_aika(meno):
                        lasna_ajat.append(meno)
            if lasna_ajat:
                return len(lasna_ajat)
        return 0

    def aika_datetimeksi(self, time_str: str) -> time:
        """Muuntaa aikamerkkijonon datetime.time -objektiksi."""
        if len(time_str) >= 5:
            if time_str[3] == "." or time_str[4] == ".":
                time_str = time_str[2:]
        if time_str == "24.00":
            return (datetime.strptime("00.00", "%H.%M") + timedelta(days=1)).time()
        return datetime.strptime(time_str, "%H.%M").time()

    def oikea_aika(self, time_str: str) -> bool:
        """Tarkistaa, että merkkijono on validi aika."""
        if not time_str.startswith(("K", "S")):
            if len(time_str) >= 5:
                if time_str[3] == "." or time_str[4] == ".":
                    time_str = time_str[2:]
            if match(r"^\d{1,2}\.\d{2}$", time_str):
                return True
        return False

    def lasna(self, paiva) -> list:
        "työntekijöiden läsnäolot (ei koulutus) tai SAK datetimet listoina: [[tulot], [lähdöt]]"
        datetime_lista = [[], []]
        if paiva in self.ajat and self.ajat[paiva] and self.ajat[paiva] != "P":
            ajat = self.ajat[paiva]
            for tulo, meno in zip(ajat[0], ajat[1]):
                if not tulo.startswith(("K", "S")):
                    if self.oikea_aika(tulo):
                        datetime_lista[0].append(self.aika_datetimeksi(tulo))
                    if self.oikea_aika(meno):
                        datetime_lista[1].append(self.aika_datetimeksi(meno))
            if len(datetime_lista[0]):
                return datetime_lista
        return []

    def uniikit(self, paiva) -> list:
        """Luo listan uniikeista ajoista päivälle, ohittaen 'S' ja 'K' alkavat merkkijonot."""
        uniikit_ajat = []
        if paiva in self.ajat and self.ajat[paiva] and self.ajat[paiva] != "P":
            ajat = self.ajat[paiva]
            for tulo, meno in zip(ajat[0], ajat[1]):
                if not tulo.startswith(("K", "S")):
                    if self.oikea_aika(tulo):
                        uniikit_ajat.append(self.aika_datetimeksi(tulo))
                    if self.oikea_aika(meno):
                        uniikit_ajat.append(self.aika_datetimeksi(meno))
            return sorted(list(set(uniikit_ajat)))
        else:
            return []


class Lapsi(Henkilo):
    def __init__(
        self,
        nimi: str,
        kutsumanimi: str,
        ryhma: str = "",
        ajat: dict = {},
        syntyma_aika: str = "",
        spessu: bool = False,
        vari: str = "",
    ):
        if syntyma_aika:
            self.syntyma_aika = datetime.strptime(syntyma_aika, "%d%m%y")
        else:
            self.syntyma_aika = datetime.now() - timedelta(days=4 * 366)

        super().__init__(nimi, kutsumanimi, ryhma, ajat)

        self.spessu = spessu
        self.vari = vari

    def aika_lkm(self, paiva) -> int:
        if paiva in self.ajat and self.ajat[paiva] != "P" and self.ajat[paiva]:
            if not isinstance(self.ajat[paiva], str):
                return sum(len(aikavali) for aikavali in self.ajat[paiva])
        return 0

    def lasna(self, paiva) -> list:
        """ei koulutusta tai sakkia"""
        # Tarkistetaan, että avain on olemassa sanakirjassa ja että sen arvo ei ole 'P'
        if paiva in self.ajat and self.ajat[paiva] != "P" and self.ajat[paiva]:
            datetime_values = [[], []]
            # Käydään läpi kaikki tulot ja lähdöt kyseisellä avaimella
            for i in range(2):
                datetime_values[i].extend(
                    [
                        datetime.strptime(time, "%H.%M").time()
                        if time != "24.00"
                        else (
                            datetime.strptime("00.00", "%H.%M") + timedelta(days=1)
                        ).time()
                        for time in self.ajat[paiva][i]
                        if match(
                            r"^\d{1,2}\.\d{2}$", time
                        )  # tarkistaa, että merkkijono vastaa muotoa 'HH.MM'
                    ]
                )
            return datetime_values
        else:
            return []

    def uniikit(self, paiva) -> list:
        uniikit_ajat = set()
        if paiva in self.ajat and self.ajat[paiva] != "P":
            for aikavali in self.ajat[paiva]:
                uniikit_ajat.update(
                    aika for aika in aikavali if aika[0] not in ["K", "S"]
                )
            time_ajat = [
                datetime.strptime(aika, "%H.%M").time() for aika in uniikit_ajat
            ]
            return sorted(time_ajat)
        else:
            return []

    def ika(self, pvm: datetime) -> int:
        if not self.syntyma_aika or self.syntyma_aika > pvm:
            return -1
        years_diff = pvm.year - self.syntyma_aika.year
        if (pvm.month, pvm.day) < (self.syntyma_aika.month, self.syntyma_aika.day):
            years_diff -= 1
        return years_diff

    def iso(self, pvm: datetime) -> bool:
        return True if self.ika(pvm) >= 3 else False

    def kerroin(self, pvm: datetime) -> float:
        return 1 / 7 if self.iso(pvm) else 1 / 4


class Ryhma:
    def __init__(
        self,
        nimi: str,
        tyontekijat: list[Tyontekija] = [],
        lapset: list[Lapsi] = [],
        vari: str = "",
        kaytossa: bool = True,
    ):
        self.nimi = nimi
        self.tyontekijat = tyontekijat or []
        self.lapset = lapset or []
        self.varit = {
            "keltainen": "yellow",
            "musta": "dark",
            "oranssi": "danger",
            "pinkki": "pink",
            "punainen": "red",
            "sininen": "primary",
            "turkoosi": "info",
            "vihreä": "success",
            "violetti": "purple",
        }
        self.vari = self.varit.get(vari)
        self.kaytossa = kaytossa

    def yhdista_ryhmat(self, ryhmat: list):
        for ryhma in ryhmat:
            self.tyontekijat.extend(ryhma.tyontekijat)
            self.lapset.extend(ryhma.lapset)
