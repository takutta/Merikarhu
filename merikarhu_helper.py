import webbrowser, os
from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go
import plotly.io as pio


# def viivat(klo, kerroin, tyontekijat, muut):
#     # Luodaan uusi viivadiagrammi
#     fig = go.Figure()

#     # Lisätään viivat yksi kerrallaan
#     fig.add_trace(go.Scatter(x=klo, y=kerroin, mode="lines", name="Kerroin"))
#     fig.add_trace(go.Scatter(x=klo, y=tyontekijat, mode="lines", name="Vastuulliset"))
#     fig.add_trace(go.Scatter(x=klo, y=muut, mode="lines", name="Muut"))

#     return fig.to_html(full_html=False)

from datetime import datetime, timedelta


def viivat(klo, kerroin, tyontekijat, muut, ryhma_nimi):
    pio.templates.default = "seaborn"  # Esimerkkinä käytetään "plotly_dark" -teemaa

    # Muunna kellonajat datetime-objekteiksi
    kellonajat = [datetime.strptime(aika, "%H:%M") for aika in klo]

    # Määritä x-akselin merkinnät puolen tunnin välein
    x_tickvals = []
    x_ticktext = []
    current_time = kellonajat[0]

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

    # Luodaan uusi viivadiagrammi
    fig = go.Figure()

    # Lisätään viivat yksi kerrallaan
    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=kerroin,
            mode="lines",
            name="Kerroin",
            line=dict(color="black"),
            hovertemplate="Kellonaika: %{x|%H:%M}<br>Kerroin: %{y}",
            connectgaps=True,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=tyontekijat,
            mode="lines",
            name="Vastuulliset",
            line=dict(color="green"),
            hovertemplate="Kellonaika: %{x|%H:%M}<br>Vastuulliset: %{y}",
            connectgaps=True,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=kellonajat,
            y=muut,
            mode="lines",
            name="Muut",
            line=dict(color="blue"),
            hovertemplate="Kellonaika: %{x|%H:%M}<br>Muut: %{y}",
            connectgaps=True,
        ),
    )

    # Aseta x-akselin merkinnät
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
                text=ryhma_nimi,  # Lisää haluamasi otsikko
                font=dict(size=24, color="black"),
            )
        ],
    )

    return fig.to_html(full_html=False)


def html_luonti(template_nimi, html_nimi, tiedot):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_nimi)
    html = template.render(data=tiedot)
    file_name = os.path.join("build", html_nimi)
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(html)
    return file_name


def html_avaus(nimi):
    filepath = "file://" + os.path.abspath(nimi)
    webbrowser.open_new_tab(filepath)
