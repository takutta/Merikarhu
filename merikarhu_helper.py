import webbrowser, os
from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go
import plotly.io as pio
from plotly.offline import plot
from datetime import datetime, timedelta
import re


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


def viivat(klo, kerroin, tyontekijat, muut, ryhma_nimi):
    pio.templates.default = "seaborn"

    kellonajat = [datetime.strptime(aika, "%H:%M") for aika in klo]

    # Määritä x-akselin merkinnät puolen tunnin välein
    x_tickvals = []
    x_ticktext = []

    if len(kellonajat) != 0:
        current_time = kellonajat[0]
    else:
        return False

    # Etsi lähin tasa- tai puolituntinen alku- ja loppuaika
    if current_time.minute >= 30:
        current_time = current_time.replace(minute=30, second=0)
    else:
        current_time = current_time.replace(minute=0, second=0)

    # Alusta x-akselin merkinnät
    while current_time <= kellonajat[-1]:
        x_tickvals.append(current_time)
        x_ticktext.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=muut,
            name="Muut",
            marker=dict(color="blue"),
            line=dict(color="blue", shape="hv"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        ),
    )

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=tyontekijat,
            name="Vastuulliset",
            marker=dict(color="green"),
            line=dict(color="green", shape="hv"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=kerroin,
            name="Kerroin",
            marker=dict(color="black"),
            line=dict(color="black", shape="hv"),
            hovertemplate=None,
            hoveron="points",
            connectgaps=True,
        )
    )

    fig.update_layout(
        yaxis=dict(dtick=1),  # Vain kokonaislukujen kohdalla
        xaxis=dict(
            tickmode="array", tickvals=x_tickvals, ticktext=x_ticktext, tickangle=45
        ),
        annotations=[
            dict(
                xref="paper",
                yref="paper",
                x=0.5,
                y=1.16,
                showarrow=False,
                text=ryhma_nimi,
                font=dict(size=24, color="black"),
            )
        ],
        hovermode="x unified",
        legend=dict(traceorder="reversed"),
    )
    return plot(fig, output_type="div", include_plotlyjs=False)


def format_date(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)


def html_luonti(template_nimi, html_nimi, data, asetukset):
    env = Environment(loader=FileSystemLoader("templates"))
    env.filters["format_date"] = format_date
    template = env.get_template(template_nimi)

    # for k, v in asetukset.items():
    #     print("key:", k, "value:", v)

    html = template.render(data=data, asetukset=asetukset)
    file_name = os.path.join("build", html_nimi)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)
    return file_name


def html_avaus(nimi):
    filepath = "file://" + os.path.abspath(nimi)
    webbrowser.open_new_tab(filepath)
