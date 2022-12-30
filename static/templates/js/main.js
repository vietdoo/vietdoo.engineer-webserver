function getRandomArrayElements(arr, count) {
    var shuffled = arr.slice(0), i = arr.length, min = i - count, temp, index;
    while (i-- > min) {
        index = Math.floor((i + 1) * Math.random());
        temp = shuffled[index];
        shuffled[index] = shuffled[i];
        shuffled[i] = temp;
    }
    return shuffled.slice(min);
}





var tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Points &copy 2012 LINZ'
    }),
    latlng = L.latLng(10.773081, 106.6829); 

var map = L.map('map', {center: latlng, zoom: 13, layers: [tiles]});

var markers = L.markerClusterGroup({ chunkedLoading: true });


// var houses = getRandomArrayElements(addressPoints, 8000);

// async function load() {
//     let url = 'http://localhost:1337/tutorials';
//     let obj = await fetch(url).json()
//     .then(text => {
//         text; // => 'Page not found'
//     });;
//     console.log(obj);
// }

// load();


async function getJSON(dist) {
    return fetch('https://vietdoo.engineer/api/v1.0/houses/?dist=' + dist)
        .then((response)=>response.json())
        .then((responseJson)=>{return responseJson});
}

async function caller() {
    const houses = await this.getJSON('Quận 5');  
    console.log('number of houses: ',houses.length);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];
        var price = houses[i]['price'];
        var img = houses[i]['img'];
        var url = houses[i]['url']
        var marker = L.marker(L.latLng(lat, long), { title: title});
        var imgStr = '<img src = "' + img +  '" style="width: 100px;" ></img>'
        var imgLink = '<a href = "' + url + '"  >Link bài viết</a>'

        var popup = title + '<h2>' + price + '</h2>' + imgStr + imgLink
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }
}

caller();

async function resetLayer() {
    markers.clearLayers();

    var radios = document.getElementsByName('district');
    var option = '';
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
            option = radios[i].value;
        }
    }

    
    
    const houses = await this.getJSON(option);  
    console.log(houses.length);
    for (var i = 0; i < houses.length; i++) {
        var lat = houses[i]['lat'];
        var long = houses[i]['long'];
        var title = houses[i]['title'];
        var price = houses[i]['price'];
        var img = houses[i]['img'];
        console.log(lat, long, title, price);
        var marker = L.marker(L.latLng(lat, long), { title: title});

        var imgStr = '<img src = "' + img +  '" style="width: 100px;" ></img>'
        var popup = title + '<h2>' + price + '</h2>' + imgStr
        marker.bindPopup(popup);
        markers.addLayer(marker);
    }
}

map.addLayer(markers);