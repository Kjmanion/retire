(function(){

    var lat = document.getElementById('mapId').dataset.lat
    var lng = document.getElementById('mapId').dataset.lng
    
    if (lat != undefined) {
        var mymap = L.map('mapId2').setView([38, -78], 6)
    } else {
        var mymap = L.map('mapId2').setView([38, -78], 6)
    }

    function populateSelects(idElement){
        console.log(idElement)
        var select = document.getElementById(idElement)
        console.log(select)
        for (i = 1950; i < 2018; i++) {
            var el = document.createElement('option')
            el.textContent = i
            el.value = i
            select.appendChild(el)
        }
    }
    populateSelects("beforeYear")
    populateSelects("afterYear")
    
    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'
    }).addTo(mymap);

    function onEachFeatures(feature, layer) {
        if (feature.properties && feature.properties.popupContent){
            layer.bindPopup('HELLOL')
        }
    }

    document.getElementById('testButt').addEventListener('click', function() {
        if (parseInt(document.getElementById('afterYear').value) > parseInt(document.getElementById('beforeYear').value)) {
            return alert ('Please check to make sure years are in the right order')
        }
        


        var item = document.getElementById('selections')
        var state = item.options[item.value-1].text
        console.log(state)
        var request = new XMLHttpRequest()
        request.open('POST', '/test', true)
        var data = {'state':state, 'afterYear':document.getElementById('afterYear').value, 'beforeYear': document.getElementById('beforeYear').value}
        var myJSON = JSON.stringify(data)
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
        request.send(myJSON)
        request.onload = function() {
            
            if (request.status >= 200 && request.status < 400) {
                var data = JSON.parse(request.responseText)
                var polyg = JSON.parse(data['result'])
                var lines = data['result2'][0]['row_to_json']
                console.log(lines)
                var lineStyle = {"color": "blue", "weight": 5,"opacity": 0.9}
                L.geoJSON(lines, {
                    style: lineStyle,
                    onEachFeature: function (feature, layer) {
                        if (feature.properties){
                            layer.bindPopup(`<h3>Date ${feature.properties.date}</h3></br><h4>F Scale : ${feature.properties.mag}</h4>`)
                        }
                    }
                }).addTo(mymap)
                var stateStyle = {"color": "black","weight": 6,"opacity": 0.5,"fill": false}
                L.geoJSON(polyg, {
                    style: stateStyle
                }).addTo(mymap)
                var coorss = JSON.parse(data['center'])
                console.log(coorss['coordinates'])
                mymap.panTo([coorss['coordinates'][1], coorss['coordinates'][0]], 6)
            } else {
            // We reached target server, but it returend nothing!
                console.log(request.status)
                console.log('we reached server, but something else failed')   
            }
        }
    })

    document.getElementById('clearing').addEventListener('click', function(){
        mymap.eachLayer(function (layer){
            console.log(layer)
            if (layer.feature && layer.feature.type != undefined){
                mymap.removeLayer(layer)
            }
            // if (layer.feature.Type == 'Feature'){
            //     mymap.removeLayer(layer)
            // }
        })
    })

})();