from random import randint, choice
from datetime import datetime, time, timedelta
import locale, math, re

# from titania_import import titania_import
from merikarhu_helper import html_luonti, html_avaus, viivat

aloitus_pvm = datetime.strptime("20.03.2023", "%d.%m.%Y")


class Aika:
    def __init__(self, paiva, tuloaika, lahtoaika):
        self.paiva = aloitus_pvm + timedelta(days=paiva)
        self.tuloaika = datetime.combine(
            self.paiva, datetime.strptime(str(tuloaika), "%H:%M").time()
        )
        self.lahtoaika = datetime.combine(
            self.paiva, datetime.strptime(str(lahtoaika), "%H:%M").time()
        )

    # TODO: Lisää SAK-aika
    # TODO: Tuo Aika, josta vähennetty SAK-aika

    def tulo(self):
        return self.tuloaika.strftime("%H:%M")

    def lahto(self):
        return self.lahtoaika.strftime("%H:%M")

    def __str__(self):
        tuloaika = self.tuloaika
        lahtoaika = self.lahtoaika.time
        return f"{self.paiva.strftime('%a')}: {self.tulo()}-{self.lahto()}"


class Tyontekija:
    def __init__(self, nimi):
        self.nimi = nimi
        self.ajat = []
        self.sak_ajat = []
        self.etunimi, self.sukunimi = self.nimi.split()
        self.kutsumanimi = self.etunimi + " " + self.sukunimi[0]
        self.vastuullinen = True

    def lisaa_aika(self, Aika):
        self.ajat.append(Aika)

    def lisaa_sak_aika(self, Aika):
        self.sak_ajat.append(Aika)

    def poista_vastuullinen(self):
        self.vastuullinen = False


# TODO
#    def lisaa_kutsumanimi(self, kutsumanimi):
#        self.kutsumanimi = kutsumanimi


class Lapsi:
    def __init__(self, nimi, syntyma_aika):
        self.nimi = nimi
        self.syntyma_aika = datetime.strptime(syntyma_aika, "%d.%m.%Y")
        self.ajat = []
        self.spessu = False
        self.etunimi, self.sukunimi = self.nimi.split()
        self.kutsumanimi = self.etunimi + " " + self.sukunimi[0]
        self.vari = ""

    def lisaa_aika(self, Aika):
        self.ajat.append(Aika)

    def lisaa_spessu(self):
        self.spessu = True

    def iso(self):
        iso = (
            aloitus_pvm.year
            - self.syntyma_aika.year
            - (
                (aloitus_pvm.month, aloitus_pvm.day)
                < (self.syntyma_aika.month, self.syntyma_aika.day)
            )
        )
        if iso >= 3:
            return True
        else:
            False

    def kerroin(self):
        if self.iso():
            return 1 / 7
        else:
            return 1 / 4


class Ryhma:
    def __init__(self, nimi):
        self.nimi = nimi
        self.tyontekijat = []
        self.lapset = []
        self.vari = ""
        self.varit = {
            "keltainen": "yellow",
            "musta": "dark",
            "oranssi": "warning",
            "pinkki": "pink",
            "punainen": "danger",
            "sininen": "primary",
            "turkoosi": "info",
            "vihreä": "success",
            "violetti": "purple",
        }

    def lisaa_tyontekija(self, tyontekija):
        self.tyontekijat.append(tyontekija)

    def lisaa_lapsi(self, lapsi):
        self.lapset.append(lapsi)

    def yhdista_ryhmat(self, ryhmat):
        for ryhma in ryhmat:
            self.tyontekijat.extend(ryhma.tyontekijat)
            self.lapset.extend(ryhma.lapset)

    def lisaa_vari(self, vari):
        self.vari = self.varit[vari]
        for lapsi in self.lapset:
            lapsi.vari = self.vari

    def __str__(self):
        tyontekijat_str = "\n".join(
            [
                f"- {tt.nimi}, työajat: {[str(ta) for ta in tt.ajat]}"
                for tt in self.tyontekijat
            ]
        )
        lapset_str = "\n".join(
            [
                f"- {ll.nimi}, ikä: {ll.ika()}, hoitoajat: {[str(ha) for ha in ll.ajat]}"
                for ll in self.lapset
            ]
        )
        return f"Ryhmä: {self.nimi}\nTyöntekijät:\n{tyontekijat_str}\nLapset:\n{lapset_str}"


# class Yhdistetty:
#     def __init__(self, nimi, ryhmat):
#         self.nimi = nimi
#         self.ryhmat = ryhmat


def listaa_lapset_tyontekijat(ryhma, paiva):
    lista = []
    uniikit = []

    for lapsi in ryhma.lapset:
        if lapsi.ajat[paiva] is not None:
            lista.append(lapsi)
            if lapsi.ajat[paiva].tuloaika not in uniikit:
                uniikit.append(lapsi.ajat[paiva].tuloaika)
            if lapsi.ajat[paiva].lahtoaika not in uniikit:
                uniikit.append(lapsi.ajat[paiva].lahtoaika)
    for tyontekija in ryhma.tyontekijat:
        if tyontekija.ajat[paiva] is not None:
            lista.append(tyontekija)
            if tyontekija.ajat[paiva].tuloaika not in uniikit:
                uniikit.append(tyontekija.ajat[paiva].tuloaika)
            if tyontekija.ajat[paiva].lahtoaika not in uniikit:
                uniikit.append(tyontekija.ajat[paiva].lahtoaika)
    uniikit.sort(key=lambda x: x)
    return lista, uniikit, paiva, ryhma


# def tiedot(lista):
#     sisalla = []
#     kellonajat = lista[1]
#     paiva = lista[2]
#     tulemattomat = lista[0]
#     viime_klo = None
#     rivi = reset_rivi()
#     aiempi_tarve = None
#     # käydään läpi kaikki kellonajat
#     for klo in kellonajat:
#         # käydään läpi sisällä olevat
#         for s in sisalla:
#             if s.ajat[paiva].lahtoaika == klo:
#                 if isinstance(s, Lapsi):
#                     rivi["lapset"] -= 1
#                 elif isinstance(s, Tyontekija):
#                     rivi["tyontekijat"] -= 1
#                 sisalla.remove(s)

#         # käydään läpi tulemattomat
#         for t in tulemattomat:
#             if t.ajat[paiva].tuloaika == klo:
#                 if isinstance(t, Lapsi):
#                     rivi["lapset"] += 1
#                 elif isinstance(t, Tyontekija):
#                     rivi["tyontekijat"] += 1
#                 sisalla.append(t)
#         # tsekataan tarvitseeko tulostaa riviä
#         if klo != viime_klo and viime_klo != None:
#             rivin_tulostus = tulosta_rivi(sisalla, rivi, viime_klo, aiempi_tarve)
#             if rivin_tulostus:
#                 aiempi_tarve = rivin_tulostus[0]
#                 print(rivin_tulostus[1])
#             rivi = reset_rivi()
#         viime_klo = klo


def jinja_tiedot(lista):
    jinja_lista = [
        [
            "klo",
            "lasten nimet",
            "lapset",
            "kerroin",
            "tt / tarve",
            "työntekijöiden nimet",
        ]
    ]
    sisalla = []
    kellonajat = lista[1]
    paiva = lista[2]
    tulemattomat = lista[0]
    viime_klo = None
    rivi = reset_rivi()
    aiempi_tarve = None
    # käydään läpi kaikki kellonajat
    for klo in kellonajat:
        # käydään läpi sisällä olevat
        for s in sisalla:
            if s.ajat[paiva].lahtoaika == klo:
                if isinstance(s, Lapsi):
                    rivi["lapset"] -= 1
                elif isinstance(s, Tyontekija):
                    rivi["tyontekijat"] -= 1
                sisalla.remove(s)

        # käydään läpi tulemattomat
        for t in tulemattomat:
            if t.ajat[paiva].tuloaika == klo:
                if isinstance(t, Lapsi):
                    rivi["lapset"] += 1
                elif isinstance(t, Tyontekija):
                    rivi["tyontekijat"] += 1
                sisalla.append(t)
        # tsekataan tarvitseeko tulostaa riviä
        if klo != viime_klo and viime_klo != None:
            rivin_tulostus = tulosta_rivi(
                sisalla, rivi, viime_klo, aiempi_tarve, lista[3].vari
            )
            if rivin_tulostus:
                aiempi_tarve = rivin_tulostus[0]
                jinja_lista.append(rivin_tulostus[1])
            rivi = reset_rivi()
        viime_klo = klo
    return jinja_lista


def reset_rivi():
    return {"tyontekijat": 0, "lapset": 0}


def tulosta_rivi(sisalla, rivi, viime_klo, aiempi_tarve, ryhma_vari):
    kertoimet = sum(tyyppi.kerroin() for tyyppi in sisalla if isinstance(tyyppi, Lapsi))
    tarve = math.ceil(kertoimet)
    if rivi != {"tyontekijat": 0, "lapset": 0} or aiempi_tarve != tarve:
        muut_summa = sum(
            isinstance(x, Tyontekija)
            for x in sisalla
            if isinstance(x, Tyontekija) and not x.vastuullinen
        )
        vastuulliset_summa = sum(
            isinstance(x, Tyontekija)
            for x in sisalla
            if isinstance(x, Tyontekija) and x.vastuullinen
        )
        pienet_summa = sum(
            isinstance(x, Lapsi)
            for x in sisalla
            if isinstance(x, Lapsi) and not x.iso()
        )
        isot_summa = sum(
            isinstance(x, Lapsi) for x in sisalla if isinstance(x, Lapsi) and x.iso()
        )
        lapset_summa = sum(isinstance(x, Lapsi) for x in sisalla)

        lapset_lista = []
        tyontekijat_lista = []
        muut_lista = []

        for x in sisalla:
            if isinstance(x, Lapsi):
                vari = x.vari if x.vari else "info"
                pieni = "rounded-0" if x.iso() else ""
                onko_spessu = (
                    f"<span class='position-absolute top-0 start-100 translate-middle p-2 bg-danger border border-light rounded-circle'><span class='visually-hidden'>New alerts</span>"
                    if x.spessu
                    else ""
                )
                lapset_lista.append(
                    f"<span class='badge text-bg-{vari} {pieni} fw-normal position-relative m-1'>{x.kutsumanimi}{onko_spessu}</span></span>"
                )
            elif isinstance(x, Tyontekija):
                if x.vastuullinen:
                    tyontekijat_lista.append(
                        f"<span class='badge text-bg-success fw-normal m-1'>{x.kutsumanimi}</span>"
                    )
                else:
                    tyontekijat_lista.append(
                        f"<span class='badge text-bg-light fw-normal m-1'>{x.kutsumanimi}</span>"
                    )
        vari_ryhma = ryhma_vari if ryhma_vari != "" else "info"
        lapset_yhteenveto = f"<span class='badge text-bg-{vari_ryhma}'>{pienet_summa}</span> + <span class='badge text-bg-{vari_ryhma} rounded-0'>{isot_summa}</span> = <span class='badge text-bg-dark'>{lapset_summa}</span>"
        spessut_paikalla = ", ".join(
            tyyppi.nimi.split()[0]
            for tyyppi in sisalla
            if isinstance(tyyppi, Lapsi) and tyyppi.spessu == True
        )
        muutos = ""
        tarve_yhteenveto = f"<span class='badge text-bg-success'>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-success'>{tarve}</span>"
        if tarve > vastuulliset_summa:
            tarve_yhteenveto = f"<span class='badge text-bg-danger '>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-dark '>{tarve}</span>"
            muutos = f"{tarve - vastuulliset_summa} liian vähän"
        elif tarve < vastuulliset_summa:
            tarve_yhteenveto = f"<span class='badge text-bg-success '>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-warning '>{tarve}</span>"
            muutos = f"{vastuulliset_summa - tarve} liian monta"
        elif vastuulliset_summa == 0 and tarve == 0 and muut_summa != 0:
            tarve_yhteenveto = f"<span class='badge text-bg-success '>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-warning '>{tarve}</span>"
            muutos = f"{vastuulliset_summa - tarve} liian monta"
        tuloste = [
            viime_klo.strftime("%H:%M"),
            "".join(lapset_lista),
            lapset_yhteenveto,
            round(kertoimet, 2),
            tarve_yhteenveto,
            "".join(tyontekijat_lista),
        ]
        return tarve, tuloste


def generoi_data():
    tyontekijat = [
        Tyontekija("Matti Meikäläinen"),
        Tyontekija("Anna Virtanen"),
        Tyontekija("Eero Koivisto"),
        Tyontekija("Helena Nieminen"),
        Tyontekija("Jani Laaksonen"),
        Tyontekija("Kaisa Hämäläinen"),
        Tyontekija("Lauri Kallio"),
        Tyontekija("Maria Saarinen"),
        Tyontekija("Niko Jokinen"),
        Tyontekija("Pia Lehtonen"),
        Tyontekija("Teemu Korhonen"),
    ]

    lapset = [
        Lapsi("Aino Mäkelä", "02.02.2022"),
        Lapsi("Eemeli Laitinen", "21.07.2018"),
        Lapsi("Helmi Lehtonen", "05.10.2021"),
        Lapsi("Ilari Rantanen", "30.01.2018"),
        Lapsi("Jenna Karjalainen", "15.12.2020"),
        Lapsi("Kaapo Niemi", "23.09.2021"),
        Lapsi("Lila Korhonen", "01.03.2022"),
        Lapsi("Mikael Peltola", "11.06.2018"),
        Lapsi("Nella Järvinen", "08.08.2020"),
        Lapsi("Oliver Virtanen", "02.04.2021"),
        Lapsi("Pihla Rautio", "27.02.2022"),
        Lapsi("Roope Salmi", "14.11.2020"),
        Lapsi("Sanni Kinnunen", "19.05.2018"),
        Lapsi("Topias Laaksonen", "08.10.2020"),
        Lapsi("Viljami Laine", "25.11.2021"),
        Lapsi("Aada Hämäläinen", "10.01.2022"),
        Lapsi("Benjamin Saarinen", "07.06.2020"),
        Lapsi("Emma Hirvensola", "15.05.2019"),
        Lapsi("Fanni Jokinen", "02.08.2019"),
        Lapsi("Gustav Korpi", "28.12.2020"),
        Lapsi("Hertta Vuorinen", "16.07.2021"),
        Lapsi("Iida Mattila", "14.03.2019"),
        Lapsi("Joona Kallio", "22.01.2021"),
        Lapsi("Kerttu Koskinen", "04.09.2020"),
        Lapsi("Lenni Aalto", "18.02.2019"),
        Lapsi("Mette Salmela", "07.03.2021"),
        Lapsi("Niilo Kärkkäinen", "29.05.2018"),
        Lapsi("Onni Niskanen", "12.12.2021"),
        Lapsi("Pinja Lindqvist", "01.01.2022"),
        Lapsi("Sara Heikkilä", "24.08.2020"),
    ]

    minuutit = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    for pv in range(7):
        for tyontekija in tyontekijat:
            random_tulo = time(randint(6, 10), choice(minuutit))
            random_lahto = time(randint(10, 18), choice(minuutit))

            tyo = Aika(
                pv,
                random_tulo.strftime("%H:%M"),
                random_lahto.strftime("%H:%M"),
            )
            random_vastuullinen = randint(0, 15)
            if random_vastuullinen == 0:
                tyontekija.poista_vastuullinen()

            tyontekija.lisaa_aika(tyo)

        for lapsi in lapset:
            random_tulo = time(randint(6, 10), choice(minuutit))
            random_lahto = time(randint(10, 18), choice(minuutit))

            hoito = Aika(
                pv,
                random_tulo.strftime("%H:%M"),
                random_lahto.strftime("%H:%M"),
            )
            random_spessu = randint(0, 15)
            if random_spessu == 0:
                lapsi.lisaa_spessu()
            lapsi.lisaa_aika(hoito)

    ryhmat = [Ryhma("Oravanpesä"), Ryhma("Pikkuoravat"), Ryhma("Siilinpiilo")]
    for i, tyontekija in enumerate(tyontekijat):
        if 2 >= i:
            ryhmat[0].lisaa_tyontekija(tyontekija)
        if 3 <= i <= 5:
            ryhmat[1].lisaa_tyontekija(tyontekija)
        if 6 <= i:
            ryhmat[2].lisaa_tyontekija(tyontekija)

    for i, lapsi in enumerate(lapset):
        if 9 >= i:
            ryhmat[0].lisaa_lapsi(lapsi)
        if 10 <= i <= 19:
            ryhmat[1].lisaa_lapsi(lapsi)
        if 20 <= i:
            ryhmat[2].lisaa_lapsi(lapsi)

    ryhmat[0].lisaa_vari("sininen")
    ryhmat[1].lisaa_vari("turkoosi")
    ryhmat[2].lisaa_vari("oranssi")
    return ryhmat


def ryhmien_yhdistys(nimi, ryhma_nimet, ryhmat):
    yhdistetty_ryhma = Ryhma(nimi)

    # Käy läpi ryhmä-instanssit
    for ryhma in ryhmat:
        # Tarkista, onko ryhmän nimi listassa
        if ryhma.nimi in ryhma_nimet:
            # Yhdistä ryhmä yhdistettyyn ryhmään
            yhdistetty_ryhma.yhdista_ryhmat([ryhma])

    # Tulosta yhdistetty ryhmä
    return yhdistetty_ryhma


# p_klo, p_kerroin, p_vastuulliset, p_muut = plotly_esityo(lapset)
def plotly_esityo(rivit):
    klo = []
    kerroin = []
    vastuulliset = []
    muut = []

    for sarake in rivit[1:]:
        klo.append(sarake[0])
        kerroin.append(sarake[3])

        numerot = re.findall(r"[0-9]+", sarake[4])
        vastuulliset_num, muut_num, tarve_num = [int(numero) for numero in numerot]
        vastuulliset.append(vastuulliset_num)
        muut.append(muut_num)

    return klo, kerroin, vastuulliset, muut


if __name__ == "__main__":
    # locale.setlocale(locale.LC_TIME, "fi_FI")
    # titania = titania_import("TPK12063.txt")
    # alkuaika, lahtoaika = aika.split("-")

    ryhmat = generoi_data()
    data = []
    yhdistetty_data = ryhmat

    koko_paivakoti = ryhmien_yhdistys(
        "Kukkumäen päiväkoti", ["Oravanpesä", "Siilinpiilo", "Pikkuoravat"], ryhmat
    )
    poop = ryhmien_yhdistys("POOP", ["Oravanpesä", "Pikkuoravat"], ryhmat)
    ryhmat.append(poop)
    ryhmat.append(koko_paivakoti)
    # "nimi1", "nimi2" --> ryhma("nimi1") & ryhma("nimi2")

    for ryhma in ryhmat:
        lista = listaa_lapset_tyontekijat(ryhma, 0)
        lapset = jinja_tiedot(lista)
        p_klo, p_kerroin, p_vastuulliset, p_muut = plotly_esityo(lapset)
        plotly_html = viivat(p_klo, p_kerroin, p_vastuulliset, p_muut, ryhma.nimi)
        ryhma_data = {
            "nimi": ryhma.nimi,
            "väri": ryhma.vari,
            "lapset": lapset,
            "kuvaaja": plotly_html,
        }
        data.append(ryhma_data)

    html_tiedosto = html_luonti("tarvetaulukko.html", "index.html", data)
    html_avaus(html_tiedosto)
