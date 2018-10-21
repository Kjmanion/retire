(function(){

    function test(inserted) {
        console.log(inserted)
    }

    var lat = document.getElementById('mapId').dataset.lat
    var lng = document.getElementById('mapId').dataset.lng
    var polyShape2 = document.getElementById('mapId').dataset.geo
    var polyShape = document.getElementById('geomCoord').textContent
   
    console.log(polyShape2.length)
    console.log(polyShape)
    if (lat != undefined) {
        var mymap = L.map('mapId2').setView([lat, lng], 6)
    } else {
        var mymap = L.map('mapId2').setView([38, -78], 6)
    }
    
    var polyg = JSON.parse(polyShape)
    console.log(polyg)
   

    // var geojsonFeature = {
    //     'type': 'Feature',
    //     "properties": {
    //         "name": "A state",
    //         "popupContent": "What the user chose"
    //     },
    //     'geometry': {
    //         'type': polyShape['type'],
    //         'coordinates': polyShape['coordinates']
    //     },
    // }
    L.geoJSON(polyg).addTo(mymap)

    // L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={pk.eyJ1IjoiZ3JpZWdpdGUiLCJhIjoiN09DU0VUMCJ9.xog8FYRRF4rbv6Y0bFMvDA}', {
    //     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    //     maxZoom: 18,
    //     id: 'mapbox.streets',
    //     accessToken: 'pk.eyJ1IjoiZ3JpZWdpdGUiLCJhIjoiN09DU0VUMCJ9.xog8FYRRF4rbv6Y0bFMvDA'
    // }).addTo(mymap);

    L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'
    }).addTo(mymap);


    
    document.getElementById('testButt').addEventListener('click', function(){
        var request = new XMLHttpRequest()
        var test = 'http://localhost/test'
        request.open('GET','/test' ,true);

        request.onload = function() {
            if (request.status >= 200 && request.status < 400) {
                var data = JSON.parse(request.responseText)
                console.log(data['result'])
                console.log(JSON.parse(data['result']))
                var polyg2 = JSON.parse(data['result'])
                var geojsonFeature = {
                    'type': 'Feature',
                    "properties": {
                        "name": "A state",
                        "popupContent": "What the user chose"
                    },
                    'geometry': polyg2
                }
                L.geoJSON(geojsonFeature).addTo(mymap)
            } else {
            // We reached target server, but it returend nothing!
                console.log(request.status)
                console.log('we reached server, but something else failed')   
            }
        }
        
        request.onerror = function() {
            console.log('connection error')
        }
        request.send()
        
    })

    document.getElementById('testButt2').addEventListener('click', function() {
        var request = new XMLHttpRequest()
        request.open('POST', '/test', true)
        var data = {'data':'Maryland'}
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
            } else {
            // We reached target server, but it returend nothing!
                console.log(request.status)
                console.log('we reached server, but something else failed')   
            }
        }


    })



})();

// var cameraLat = JSON.parse(document.getElementById('mapId').dataset.lat);
// var cameraLon = JSON.parse(document.getElementById('mapId').dataset.lng); 