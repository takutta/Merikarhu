let siirraAlas = true;
$(document).ready(function () {
    $("#toggleLapset").click(function () {
        $("th:nth-child(2), td:nth-child(2)").toggle();
        const sections = document.getElementsByClassName('toggle-section');
        $("th:nth-child(6), td:nth-child(6)").toggle();
        for (let i = 0; i < sections.length; i++) {
            sections[i].classList.toggle('ryhma');
        }
        //yläpalkki mini-moodissa
        var navbarToggler = document.getElementById("navbarToggler");
        var collapseButton = document.getElementById("collapseButton");

        if (navbarToggler.style.display === "none") {
            collapseButton.style.setProperty("opacity", "1", "");
            navbarToggler.style.setProperty("display", "", "");
        } else {
            collapseButton.style.setProperty("opacity", "0", "");
            navbarToggler.style.setProperty("display", "none", "important");
        }

        


        // Kuvaajat
        let i = 1;
        while (true) {
            let ala = document.getElementById(`${i}_kuvaajaAla`);
            let yla = document.getElementById(`${i}_kuvaajaYla`);

            // Jos ala tai yla ei ole olemassa, lopeta silmukka
            if (!ala || !yla) {
                break;
            }

            if (siirraAlas) {
                while (yla.firstChild) {
                    ala.appendChild(yla.firstChild);
                }
            } else {
                while (ala.firstChild) {
                    yla.appendChild(ala.firstChild);
                }
            }

            i++;
        }
        siirraAlas = !siirraAlas;
    });

      
    
});

