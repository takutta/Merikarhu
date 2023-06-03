$(document).ready(function () {
    $('button[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
        for (var i = 0; i < 7; i++) {
            for (var j = 1; j < 6; j++) {
                var kuvaajaYlaId = i.toString() + j.toString() + '_kuvaajaYla';
                var kuvaajaAlaId = i.toString() + j.toString() + '_kuvaajaAla';

                var kuvaajaYla = document.getElementById(kuvaajaYlaId);
                var kuvaajaAla = document.getElementById(kuvaajaAlaId);
                console.log(kuvaajaYlaId + kuvaajaYla)
                
                if(kuvaajaYla && kuvaajaYla.children.length > 0 && kuvaajaYla.children[0].id){
                    var plotlyYlaId = kuvaajaYla.children[0].id;
                    Plotly.Plots.resize(plotlyYlaId);
                }
                
                if(kuvaajaAla && kuvaajaAla.children.length > 0 && kuvaajaAla.children[0].id){
                    var plotlyAlaId = kuvaajaAla.children[0].id;
                    Plotly.Plots.resize(plotlyAlaId);
                }
                if(kuvaajaYla && kuvaajaYla.children.length > 0 && kuvaajaYla.children[0].children[0].id){
                    var plotlyYlaId = kuvaajaYla.children[0].children[0].id;
                    Plotly.Plots.resize(plotlyYlaId);
                }
                
                if(kuvaajaAla && kuvaajaAla.children.length > 0 && kuvaajaAla.children[0].children[0].id){
                    var plotlyAlaId = kuvaajaAla.children[0].children[0].id;
                    Plotly.Plots.resize(plotlyAlaId);
                }
            }
        }
    });
});
