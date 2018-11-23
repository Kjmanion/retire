(function(){

    var lat = document.getElementById('mapId').dataset.lat
    var lng = document.getElementById('mapId').dataset.lng
    var polyShape2 = document.getElementById('mapId').dataset.geo
    var polyShape = document.getElementById('geomCoord').textContent
   
    console.log(polyShape2.length)
    console.log(polyShape)
    if (lat != undefined) {
        var mymap = L.map('mapId2').setView([38, -78], 6)
    } else {
        var mymap = L.map('mapId2').setView([38, -78], 6)
    }
    
   
    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'
    }).addTo(mymap);

    document.getElementById('testButt2').addEventListener('click', function() {
        var item = document.getElementById('selections')
        var state = item.options[item.value-1].text
        var request = new XMLHttpRequest()
        request.open('POST', '/test', true)
        var data = {'data':state}
        var myJSON = JSON.stringify(data)
        request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8')
        request.send(myJSON)
        request.onload = function() {
            
            if (request.status >= 200 && request.status < 400) {
                var data = JSON.parse(request.responseText)
                console.log(data)
                console.log(data['result'])
                var polyg = JSON.parse(data['result'])
                L.geoJSON(polyg).addTo(mymap)
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

})();