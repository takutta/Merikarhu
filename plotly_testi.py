from jinja2 import Environment, FileSystemLoader
import plotly.graph_objects as go
import webbrowser

# Luo x- ja y-koordinaatit jokaiselle viivalle
x = [1, 2, 3, 4, 5]
y1 = [1, 3, 2, 4, 3]
y2 = [2, 4, 1, 3, 2]
y3 = [3, 2, 4, 1, 4]


# Luo jokainen viiva erillisenä jäljityksenä (trace)
trace1 = go.Scatter(x=x, y=y1, mode="lines", name="Viiva 1")
trace2 = go.Scatter(x=x, y=y2, mode="lines", name="Viiva 2")
trace3 = go.Scatter(x=x, y=y3, mode="lines", name="Viiva 3")

# # Luo datalista, joka sisältää kaikki viivat
traces = [trace1, trace2, trace3]

# # Lataa Jinja-ympäristö ja lataa mallitiedosto
env = Environment(loader=FileSystemLoader("."))
template = env.get_template("plotly_template.jinja")

# # Renderöi malli ja anna datamuuttujat mallille
output = template.render(traces=traces)

# # Renderöi malli ja anna datamuuttujat mallille
output = template.render(x=x, y=y)

html_filename = "plotly_tuotos.html"

# # Tallenna lopullinen HTML-tiedosto
with open(html_filename, "w") as file:
    file.write(output)


# # Määritä Vivaldi-selain
vivaldi_path = r"C:\Users\pampi\AppData\Local\Vivaldi\Application\vivaldi.exe"  # Määritä oikea polku Vivaldi-selaimelle

# # Aseta Vivaldi-selain webbrowser-moduulille
webbrowser.register("vivaldi", None, webbrowser.BackgroundBrowser(vivaldi_path))

# # Avaa HTML-tiedosto Vivaldi-selaimessa
webbrowser.get("vivaldi").open(
    "file://" + r"c:\Users\pampi\Documents\dev\Merikarhu\plotly.html"
)
