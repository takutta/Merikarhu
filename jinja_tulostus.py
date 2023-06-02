from jinja2 import Template


def jinja_template(data):
    # Jinja-templaatti
    template = Template(
        """
    <!doctype html>
<html lang="en">
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Merikarhun jätökset</title>
        <link rel="stylesheet" href="minty.min.css">
        <style>
            .text-bg-yellow {background-color: #ffff00}
            .text-bg-pink {background-color: #e91e63}
            .text-bg-teal {background-color: #009688}
            .text-bg-purple {background-color: 6200ea}
            .text-bg-primary {background-color: #2962ff}
            
            .text-yellow {background-color: #ffff00}
            .text-pink {background-color: #e91e63}
            .text-teal {background-color: #009688}
            .text-purple {background-color: 6200ea}
            .text-primary {background-color: #2962ff}
            .nav-pills .nav-link.active, .nav-pills .show>.nav-link {background-color:rgba(0,0,0,0.4)}
            .minwidth145 {min-width: 145px}
            .retroshadow {
                
                text-shadow: 2px 2px 0px rgba(0,0,0,0.4), 0px 0px 0px rgba(255,255,255,1), 0px 0px 4px rgba(0,0,0,1);
            }
            .ryhma {
                float:left;
                min-width:400px;
                margin-right:10px
            }
            
        </style>        
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script>
            $(document).ready(function() {
                $("#toggleLapset").click(function() {
                    $("th:nth-child(2), td:nth-child(2)").toggle();
                    const sections = document.getElementsByClassName('toggle-section');
                    $("th:nth-child(6), td:nth-child(6)").toggle();
                    for (let i = 0; i < sections.length; i++) {
                        sections[i].classList.toggle('ryhma');
                    }
                });
            });
            

        </script>
        
    </head>
    <body data-bs-spy="scroll" data-bs-target="#navbar-spy">
        <div class="sticky-md-top">
            <nav id="navbar-spy" class="navbar navbar-dark navbar-expand-xl pt-0 bg-dark bg-body-tertiary">
                <div class="container-fluid d-flex">
                    <h1 class="navbar-brand retroshadow mt-2 ps-3 fs-3 py-0 my-0 text-white fw-bold" href="#">Merikarhu</h1>
                    
                    <div class="me-2">
                        <input type="checkbox" class="btn-check" id="toggleLapset" autocomplete="off">
                        <label class="btn mt-2 btn-outline-info" for="toggleLapset">Mini</label>
                    </div>
                    
                    <button class="navbar-toggler ms-auto mt-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggler" aria-controls="navbarToggler" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    
                    <ul id="navbarToggler" class="collapse navbar-collapse nav nav-pills">
                        {% for ryhmä in data %}
                        <li class="nav-item">
                            <a class="nav-link mt-2 me-2" href="#{{ ryhmä["nimi"].replace(' ', '_').replace('ä', 'a').replace('ö', 'o') }}">{{ryhmä["nimi"]}}</a>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </nav>
        </div>
        <div class="container-fluid">
            <div data-bs-spy="scroll" data-bs-target="#navbar-spy" data-bs-root-margin="0px 0px -40%" data-bs-smooth-scroll="true" class="bg-body-tertiary px-3 pt-2 rounded-2" tabindex="0">
                        {% for ryhmä in data %}
                <section id="{{ ryhmä["nimi"].replace(' ', '_').replace('ä', 'a').replace('ö', 'o') }}" class="toggle-section">
                    <h2>{{ ryhmä["nimi"] }}</h2>
                    <div class="row">
                        <div class="">
                            <table class="table table-striped table-bordered">
                                <thead class="table-dark">
                                    <tr>
                                        {% for otsikko in ryhmä["lapset"][0] %}
                                        <th scope="col" class="{% if otsikko == "tt / tarve" or otsikko == "lapset" %}minwidth145{% endif %}">{{otsikko}}</th>
                                        {% endfor %}
                                    </tr>
                                </thead>
                                <tbody>
                            {% for row in ryhmä["lapset"][1:] %}
                                <tr>
                                {% for item in row %}
                                    <td>{{ item }}</td>
                                {% endfor %}
                                </tr>
                            {% endfor %}</tbody>
                            </table>
                            
                        </div>
                    </div>
                </section>
        {% endfor %}
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
    </body>
    </html>
    """
    )

    html_tulostus("merikarhu.html", template.render(data=data))
