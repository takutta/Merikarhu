from random import randint, choice, shuffle
from datetime import datetime, time, timedelta
import locale, math
from luokat import Henkilo, Lapsi, Tyontekija, Ryhma
import titania as ti
import excel as ex
import merikarhu_helper as helper


def listaa_lapset_tyontekijat(ryhma, paiva, ero):
    """
    Kerätään lapset & työntekijät listalle ja uniikit tulot & menot omalle listalleen
    """
    lista = []
    uniikit = []

    for lapsi in ryhma.lapset:
        if lapsi.aika_lkm(paiva - ero):
            lista.append(lapsi)
            for aika in lapsi.uniikit(paiva - ero):
                if aika not in uniikit:
                    uniikit.append(aika)

    for tt in ryhma.tyontekijat:
        lkm = tt.lasna_lkm(paiva)
        jutut = tt.lasna(paiva)
        if tt.lasna_lkm(paiva):
            lista.append(tt)
            for aika in tt.uniikit(paiva):
                if aika not in uniikit:
                    uniikit.append(aika)
    return lista, sorted(uniikit), paiva, ryhma


def tiedot(lista_lapset_tyontekijat, uniikit, paiva, ryhma, pvm, ero):
    """Pitää yllä listoja lasten läsnäoloista"""
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
    kellonajat = uniikit
    tulemattomat = lista_lapset_tyontekijat
    viime_klo = None
    rivi = reset_rivi()
    aiempi_tarve = None
    # käydään läpi kaikki kellonajat
    for klo in kellonajat:
        for s in sisalla.copy():
            # ei enää sisällä jos lähtöaika sama kuin klo
            if isinstance(s, Tyontekija):
                ajat = s.lasna(paiva)
                if ajat:
                    for lahto in ajat[1]:
                        if lahto == klo:
                            rivi["tyontekijat"] -= 1
                            sisalla.remove(s)
            elif isinstance(s, Lapsi):
                ajat = s.lasna(paiva - ero)
                if ajat:
                    for lahto in ajat[1]:
                        if lahto == klo:
                            rivi["lapset"] -= 1
                            sisalla.remove(s)

        for t in tulemattomat:
            if isinstance(t, Tyontekija):
                ajat = t.lasna(paiva)
                if ajat:
                    for tulo in ajat[0]:
                        if tulo == klo:
                            rivi["tyontekijat"] += 1
                            if t not in sisalla:
                                sisalla.append(t)
            elif isinstance(t, Lapsi):
                ajat = t.lasna(paiva - ero)
                if ajat:
                    for tulo in ajat[0]:
                        if tulo == klo:
                            rivi["lapset"] += 1
                            if t not in sisalla:
                                sisalla.append(t)

        # tsekataan tarvitseeko tulostaa riviä
        rivin_tulostus = tulosta_rivi(sisalla, rivi, klo, aiempi_tarve, ryhma.vari, pvm)
        if rivin_tulostus:
            aiempi_tarve = rivin_tulostus[0]
            jinja_lista.append(rivin_tulostus[1])
        rivi = reset_rivi()
        # viime_klo = klo
    return jinja_lista


def reset_rivi() -> dict[str, int]:
    """Rivin nollaus"""
    return {"tyontekijat": 0, "lapset": 0}


def tulosta_rivi(sisalla, rivi, viime_klo, aiempi_tarve, ryhma_vari, pvm):
    """Kirjoittaa rivin taulukkoon"""
    kertoimet = sum(
        henkilo.kerroin(pvm) for henkilo in sisalla if isinstance(henkilo, Lapsi)
    )
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
            if isinstance(x, Lapsi) and not x.iso(pvm)
        )
        isot_summa = sum(
            isinstance(x, Lapsi) for x in sisalla if isinstance(x, Lapsi) and x.iso(pvm)
        )
        lapset_summa = sum(isinstance(x, Lapsi) for x in sisalla)

        lapset_lista = []
        tyontekijat_lista = []
        muut_lista = []

        for x in sisalla:
            if isinstance(x, Lapsi):
                vari = x.vari if x.vari else "info"
                pieni = "rounded-0" if x.iso(pvm) else ""
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
        if not ryhma_vari:
            ryhma_vari = "info"
        lapset_yhteenveto = f"<span class='badge text-bg-{ryhma_vari}'>{pienet_summa}</span> + <span class='badge text-bg-{ryhma_vari} rounded-0'>{isot_summa}</span> = <span class='badge text-bg-dark'>{lapset_summa}</span>"
        spessut_paikalla = ", ".join(
            henkilo.kutsumanimi
            for henkilo in sisalla
            if isinstance(henkilo, Lapsi) and henkilo.spessu == True
        )

        if vastuulliset_summa == 0 and tarve == 0 and muut_summa != 0:
            tarve_yhteenveto = f"<span class='badge text-bg-success '>{vastuulliset_summa}</span> + <span class='badge text-bg-warning '>{muut_summa}</span> / <span class='badge text-bg-success '>{tarve}</span>"
        elif vastuulliset_summa != 0 and tarve == 0 and muut_summa != 0:
            tarve_yhteenveto = f"<span class='badge text-bg-warning '>{vastuulliset_summa}</span> + <span class='badge text-bg-warning '>{muut_summa}</span> / <span class='badge text-bg-success '>{tarve}</span>"
        elif tarve > vastuulliset_summa:
            tarve_yhteenveto = f"<span class='badge text-bg-dark '>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-danger '>{tarve}</span>"
        elif tarve < vastuulliset_summa:
            tarve_yhteenveto = f"<span class='badge text-bg-warning '>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-success '>{tarve}</span>"
        else:
            tarve_yhteenveto = f"<span class='badge text-bg-success'>{vastuulliset_summa}</span> + <span class='badge text-bg-light '>{muut_summa}</span> / <span class='badge text-bg-success'>{tarve}</span>"
        tuloste = [
            viime_klo.strftime("%H:%M"),
            "".join(lapset_lista),
            lapset_yhteenveto,
            round(kertoimet, 2),
            tarve_yhteenveto,
            "".join(tyontekijat_lista),
        ]
        return tarve, tuloste


def lisaa_yhdistetyt_ryhmat(data, ryhmat, tyontekijat):
    kaikki_ryhmat = []
    # Koko päiväkoti
    koko_paivakoti = ryhmien_yhdistys(
        "Päiväkoti", [ryhma.nimi for ryhma in ryhmat], ryhmat
    )
    tt_ilman_ryhmaa = [tt for tt in tyontekijat if tt.ryhma and tt.ryhma != "Ei"]
    koko_paivakoti.tyontekijat.extend(tt_ilman_ryhmaa)
    kaikki_ryhmat.append(koko_paivakoti)

    # Yhdistetyt ryhmät
    for yhd in data["yhdistetyt_ryhmat"]:
        yhd_nimi = yhd["nimi"]
        yhd_nimet = yhd["ryhman_nimet"]
        yhd_vari = yhd.get("vari")
        yhd_ryhma = ryhmien_yhdistys(yhd_nimi, yhd_nimet, ryhmat, yhd_vari)
        ryhmat.append(yhd_ryhma)
    # koko päiväkoti ensimmäiseksi. sitten muut ryhmät aakkosjärjestyksessä
    ryhmat.sort(key=lambda ryhma: ryhma.nimi)
    kaikki_ryhmat.extend(ryhmat)
    return kaikki_ryhmat


def ryhmien_yhdistys(nimi, ryhma_nimet, ryhmat, vari=None):
    yhdistetty_ryhma = Ryhma(nimi)

    yhdistettavat = [ryhma for ryhma in ryhmat if ryhma.nimi in ryhma_nimet]
    yhdistetty_ryhma.yhdista_ryhmat(yhdistettavat)

    if vari:
        yhdistetty_ryhma.vari = ryhmat[0].varit.get(vari)

    return yhdistetty_ryhma


def paivien_luoja(e_asetukset, pvm_titania):
    """Oikeat päivämäärät viikolle"""
    ti_pvm = datetime.strptime(pvm_titania, "%d.%m.%y")
    e_pvm = str(e_asetukset["pvm"]) + "." + str(pvm_titania[-2:])
    e_pvm = datetime.strptime(e_pvm, "%d.%m.%y")
    ero = e_pvm - ti_pvm
    lista_paivista = []
    for i in range(e_asetukset["paivat"]):
        uusi_pvm = e_pvm + timedelta(days=i)
        lista_paivista.append(uusi_pvm)
    return lista_paivista, ero.days


def ryhmien_luonti(tt_data):
    """Lapset, työntekijä ja ryhmät instanssien luonti"""
    lapset = []
    tyontekijat = []
    ryhmat = []
    for l in tt_data["lapset"]:
        if l.get("nimi"):
            lapsi = Lapsi(
                l["nimi"],
                l["kutsumanimi"],
                l["ryhma"],
                l["ajat"],
                l["syntyma_aika"],
                l["spessu"],
            )
            lapset.append(lapsi)
    for tt in tt_data["tyontekijat"]:
        if tt.get("kokonimi"):
            tyontekija = Tyontekija(
                tt["kokonimi"],
                tt["kutsumanimi"],
                tt.get("ryhma"),
                tt["ajat"],
                tt.get("vastuullinen"),
            )
            tyontekijat.append(tyontekija)
    for r in tt_data["ryhmat"]:
        if r.get("nimi"):
            ryhman_tt = [tt for tt in tyontekijat if tt.ryhma == r["nimi"]]
            ryhman_l = [l for l in lapset if l.ryhma == r["nimi"]]
            ryhma = Ryhma(
                r["nimi"], ryhman_tt, ryhman_l, r.get("vari"), r.get("kaytossa_mk")
            )

            # asettaa ryhmän värin jokaiselle lapselle ryhmässä
            for lapsi in ryhman_l:
                lapsi.vari = ryhma.varit.get(r.get("vari"))
            ryhmat.append(ryhma)

    return lapset, tyontekijat, ryhmat


def luo_tarvetaulukko(data, pvm_titania):
    lapset, tyontekijat, ryhmat = ryhmien_luonti(data)

    paiva_lista, ero = paivien_luoja(data, pvm_titania)
    asetukset = {"viikon_paivat": paiva_lista, "ero": ero}

    ryhmat = lisaa_yhdistetyt_ryhmat(data, ryhmat, tyontekijat)

    viikko_data = {}
    for paiva in range(ero, ero + len(paiva_lista)):
        paiva_data = []
        ryhmat_kaytossa = [ryhma for ryhma in ryhmat if ryhma.kaytossa]

        for ryhma in ryhmat_kaytossa:
            lista, uniikit, paiva, ryhma = listaa_lapset_tyontekijat(ryhma, paiva, ero)
            rivit = tiedot(lista, uniikit, paiva, ryhma, paiva_lista[paiva - ero], ero)
            # kuvaaja
            p_klo, p_kerroin, p_vastuulliset, p_muut = helper.plotly_esityo(rivit)
            plotly_html = helper.viivat(
                p_klo, p_kerroin, p_vastuulliset, p_muut, ryhma.nimi
            )

            ryhma_data = {
                "nimi": ryhma.nimi,
                "väri": ryhma.vari,
                "lapset": rivit,
                "kuvaaja": plotly_html,
            }
            paiva_data.append(ryhma_data)
            viikko_data[paiva - ero] = paiva_data

    html_tiedosto = helper.html_luonti(
        "tarvetaulukko.jinja", f"index.html", viikko_data, asetukset
    )
    helper.html_avaus(html_tiedosto)


if __name__ == "__main__":
    # kkm
    # df1, pvm_titania = ti.titania_import(r"C:\Users\pampi\Downloads\HON01093.txt")
    # titania_tt = ti.df_to_json(df1)

    # tapiola 1073
    # df1, pvm_titania = ti.titania_import(r"C:\Users\pampi\Downloads\TAP01073.txt")
    # tt1 = ti.df_to_json(df1)
    # df2 = ti.titania_import(r"C:\Users\pampi\Downloads\TPK12073.txt")
    # tt2 = ti.df_to_json(df2[0])
    # titania_tt = ti.yhdista_tyontekijat([tt1, tt2])

    # tapiola uusi lista
    df1, pvm_titania = ti.titania_import(
        r"C:\Users\pampi\Documents\dev\Hoitoajat\esimerkki\titania1.txt"
    )

    tt1 = ti.df_to_json(df1)
    df2 = ti.titania_import(
        r"C:\Users\pampi\Documents\dev\Hoitoajat\esimerkki\titania2.txt"
    )
    tt2 = ti.df_to_json(df2[0])
    titania_tt = ti.yhdista_tyontekijat([tt1, tt2])

    excel_data = ex.lataa_json(r"C:\Users\pampi\merikarhu\input\merikarhu_input.json")

    data = ex.tt_asetukset_synkka(titania_tt, excel_data)
    ex.excel_export(data, r"C:\Users\pampi\merikarhu\output\merikarhu_output.json")
    luo_tarvetaulukko(data, pvm_titania)
