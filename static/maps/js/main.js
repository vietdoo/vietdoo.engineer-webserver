var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
    }),
    latlng = L.latLng(10.773081, 106.6829); 

var map = L.map('map', {center: latlng, zoom: 13, layers: [tiles]});
var markers = L.markerClusterGroup({ chunkedLoading: true });

function makePopup(house) {
    var title = house['title'];
    var price = house['price'];
    var url = house['url']
    var img = house['img'];
    var imgStr = '<img src = "' + img +  '" style="width: 120px;" ></img>'
    var imgLink = '<a href = "' + url + '">Chi tiết</a>'

    return title + '<h2>' + price + '</h2>' + imgStr + imgLink
}

async function getJSON(dist) {
    return fetch('https://vietdoo.engineer/api/v1.0/houses/?dist=' + dist)
        .then((response)=>response.json())
        .then((responseJson)=>{return responseJson});
}

async function caller() {
    var startTime = performance.now()
    const houses = await this.getJSON('Quận 5');  
    console.log("Successfully request: ", houses.length, " houses in ", houses[0]['dist']);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];

        var marker = L.marker(L.latLng(lat, long), { title: title});

        var popup = makePopup(houses[i]);
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }
    console.log("Done in ", performance.now() - startTime, " ms")
}

caller();

async function resetLayer() {
    markers.clearLayers();

    var startTime = performance.now()

    var radios = document.getElementsByName('district');
    var option = '';
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            option = radios[i].value;
        }
    }
    
    const houses = await this.getJSON(option);  
    console.log("Successfully request: ", houses.length, " houses in ", houses[0]['dist']);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses['title'];

        var marker = L.marker(L.latLng(lat, long), { title: title});
        var popup = makePopup(houses[i]);
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }
    console.log("Done in ", performance.now() - startTime, " ms")
}

map.addLayer(markers);