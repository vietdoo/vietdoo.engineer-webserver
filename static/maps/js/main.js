function numberWithCommas(x) {
    if (x !== null) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
}

$(function() {
    $( "#slider-range" ).slider({
        range: true,
        min: 100000000,
        max: 10000000000,
        values: [ 100000000, 10000000000 ],
        slide: function( event, ui ) {
            $( "#min-range" ).html(numberWithCommas(ui.values[ 0 ]) );
            $( "#max-range" ).html(ui.values[ 1 ] == 10000000000?numberWithCommas(ui.values[ 1 ]) + ' +' : numberWithCommas(ui.values[ 1 ]) );
            // $( "#lowInput" ).value = $( "#min" ).innerHTML.replace(/,/g, '');
            // $( "#highInput" ).value = $( "#max" ).innerHTML.replace(/,/g, '');
        }
    });

    //slider range data tooltip set
    // var $handler = $("#slider-range .ui-slider-handle");

    // $handler.eq(0).append("<b class='amount'><span id='min'>"+numberWithCommas($( "#slider-range" ).slider( "values", 0 )) +"</span> đ</b>");
    // $handler.eq(1).append("<b class='amount'><span id='max'>"+numberWithCommas($( "#slider-range" ).slider( "values", 1 )) +"</span> đ</b>");

    //slider range pointer mousedown event
    $handler.on("mousedown",function(e){
        e.preventDefault();
        $(this).children(".amount").fadeIn(300);
    });

    //slider range pointer mouseup event
    $handler.on("mouseup",function(e){
        e.preventDefault();
        $(this).children(".amount").fadeOut(300);
    });
    console.log(numberWithCommas($( "#slider-range" ).slider( "values", 0 )));
});
    


// slider-end

var tiles = L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}{r}.{ext}', {
	attribution: ' Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
	subdomains: 'abcd',
	minZoom: 0,
	maxZoom: 18,
	ext: 'png'
}),
    latlng = L.latLng(10.773081, 106.6829); 

var map = L.map('map', {center: latlng, zoom: 13, layers: [tiles]});
map.attributionControl.setPrefix('Python Project')
var markers = L.markerClusterGroup({ chunkedLoading: true });
const numberRandomHouse = 20;


function makePopup(house) {
    var title = house['title'];
    var price = house['price'];
    var url = house['url']
    var img = house['img'];
    var imgStr = '<img src = "' + img +  '" style="width: 100px; height: 100px; object-fit: cover;" ></img>'
    var imgLink = '<button class="my-btn" role="button"><a href = "' + url + '" target="_blank" " style="text-decoration: none;"> Chi tiết</a></button>'

    return '<div class="row"><div class="column1" style="">' + imgStr + '</div><div class="column2" style="">' + title + '<h3>' + numberWithCommas(price) + ' VND</h3>' + imgLink + '</div></div>'
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function makeAdvertise(house) {
    var title = house['title'];
    var price = house['price'];
    var url = house['url']
    var img = house['img'];
    var rooms = house['rooms'];
    var size = house['size'];
    var imgStr = '<img src = "' + img +  '" style="width: 100%; height: 150px; object-fit: cover; border-radius: 5px;" ></img>'
    var imgLink = '<button class="my-btn" role="button"><a href = "' + url + '" target="_blank" " style="text-decoration: none;"> Chi tiết</a></button>'

    return imgStr + '<div style="margin: 10px;">' + '<div style="min-height: 90px;"><h3>' + numberWithCommas(price) + ' VND</h3>' + '<p style="font-size: 0.8em; color: #7c7c7c; margin-top: 10px;">' + title + '</p></div>' + '<div style="margin-bottom: 5px;"><span style="color: #7c7c7c;margin-right: 10px;"><img width="20px" height="20px" style="margin-bottom: -3px; margin-right: 5px; color: #7c7c7c;" src="./static/maps/assets/images/door.png"></img><span style="font-size: 0.8em; margin-left: 3px;">Phòng: ' + rooms + '</span></span></div>' + '<div><span style="color: #7c7c7c; margin-left: 3px;"><img width="20px" height="20px" style="margin-bottom: -3px; margin-right: 5px; color: #7c7c7c;" src="./static/maps/assets/images/square.png"></img><span style="font-size: 0.8em;">Diện tích: ' + size + ' m<sup>2</sup></span></span></div>' + imgLink + '</div>'
}

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
// https://vietdoo.engineer/api/v1.0/houses/?dist=Qu%E1%BA%ADn%204&low=1920000000&high=2200000000
async function getJSON(dist, low, high) {
    if (low !== 0 && high !== 0) {
        return fetch('https://vietdoo.engineer/api/v1.0/houses/?dist=' + dist + '&low=' + low + '&high=' + high)
            .then((response)=>response.json())
            .then((responseJson)=>{return responseJson});
    }
    return fetch('https://vietdoo.engineer/api/v1.0/houses/?dist=' + dist)
            .then((response)=>response.json())
            .then((responseJson)=>{return responseJson});
}

async function caller() {
    var startTime = performance.now()
    const houses = await this.getJSON('Quận 1','','');  

    var quantityString = "";
    quantityString = '<h2>' + houses.length + '</h2>  Ngôi nhà được tìm thấy';
    document.getElementById("quantity").innerHTML = quantityString;

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

    var agents = getRandomArrayElements(houses, numberRandomHouse);
    var inner = "";
    for(var i = 0; i < numberRandomHouse; i++) {
        var agentInner = '<div class="house">' + makeAdvertise(agents[i]) + '</div>';
        inner += agentInner;
    }

    document.getElementById("house-container").innerHTML = inner;

    console.log("Done in ", performance.now() - startTime, " ms");
}

caller();

async function resetLayer() {
    markers.clearLayers();

    var startTime = performance.now()

    var selectDistrict = document.getElementById('district');

    var minPrice = document.getElementById('min-range').innerHTML.split('.').join("").replace(/,/g, '');
    var maxPrice = document.getElementById('max-range').innerHTML.split('.').join("").replace(/,/g, '');


    console.log(maxPrice);
    if (maxPrice == 10000000000 || maxPrice === '10000000000 +') {
        maxPrice = 1000000000000000;
        console.log("10 tyyyy+++");
    }


    var optionDistrict = '';
    optionDistrict = selectDistrict.value;

    const houses = await this.getJSON(optionDistrict, minPrice, maxPrice); 

    var agents = [];

    if (houses.length > numberRandomHouse) {
        agents = getRandomArrayElements(houses, numberRandomHouse);
    }
    else {
        agents = houses;
    }

    var inner = "";

    for(var i = 0; i < agents.length; i++) {
        var agentInner = '<div class="house" style="">' + makeAdvertise(agents[i]) + '</div>';
        inner += agentInner;
    }

    document.getElementById("house-container").innerHTML = inner;

    var quantityString = "";
    quantityString = '<h2>' + houses.length + '</h2>  Ngôi nhà được tìm thấy';
    document.getElementById("quantity").innerHTML = quantityString;

    document.getElementById("quantity").innerHTML = quantityString;

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
