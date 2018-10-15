(function() {

    var loggedUser;
    firebase.auth().onAuthStateChanged(firebaseUser=>{
        if (!firebaseUser) {
            location.href="index.html";
        }
        // Se cargan los datos del usuario en la cabecera
        document.getElementById("usuario").innerHTML = firebaseUser.email;
        cargarSpinner(firebaseUser.uid);
        loggedUser = firebaseUser;
    });

    const btnLogout          = document.getElementById("btnLogout"); 
    const btnNewCar          = document.getElementById("newCar");
    const btnEditCar         = document.getElementById("editCar");
    const btnCarroRegistrar  = document.getElementById("btnCarroRegistrar");
    
    // Editar vehículo
    btnEditCar.addEventListener('click', e=>{
        document.getElementById("carro").style.display = 'block';
        document.getElementById("txtCarroNombre").value = document.getElementById("vehiculos").options[document.getElementById("vehiculos").selectedIndex].text;
        document.getElementById("txtCarroPlaca").value = document.getElementById("placa").innerHTML;
        document.getElementById("txtCarroPlaca").readOnly = true;
        document.getElementById("txtCarroIMEI").value = document.getElementById("imei").innerHTML;
        document.getElementById("txtCarroIMEI").readOnly = true;
        document.getElementById("txtCarroTelefono").value = document.getElementById("phone").innerHTML;
        document.getElementById("txtCarroPassword").value = document.getElementById("password").innerHTML;
    });
    
    // Guardar vehículo
    btnCarroRegistrar.addEventListener('click', e=>{
        const txtCarroNombre = document.getElementById("txtCarroNombre").value;
        const txtCarroPlaca = document.getElementById("txtCarroPlaca").value;
        const txtCarroIMEI = document.getElementById("txtCarroIMEI").value;
        const txtCarroTelefono = parseFloat(document.getElementById("txtCarroTelefono").value);
        const txtCarroPassword = parseInt(document.getElementById("txtCarroPassword").value);
    
        if (txtCarroNombre=="") {
            console.log("El campo nombre es obligatorio");
            return 0;
        }

        if (txtCarroPlaca=="") {
            console.log("El campo placa es obligatorio");
            return 0;
        }

        if (txtCarroIMEI=="") {
            console.log("El campo IMEI es obligatorio");
            return 0;
        }

        if (txtCarroTelefono=="") {
            console.log("El campo teléfono es obligatorio");
            return 0;
        }

        if (txtCarroPassword=="") {
            console.log("El campo password es obligatorio");
            return 0;
        }    
    
        firebase.database().ref("Vehiculos/"+txtCarroPlaca).set({
            activo: "1",
            idUsuario: loggedUser.uid,
            nombre: txtCarroNombre,
            placa: txtCarroPlaca,
            password: txtCarroPassword,
            telefono: txtCarroTelefono,
            imei: txtCarroIMEI
        });
        
        alert("El vehículo "+txtCarroNombre+" ha sido registrado en la DB.");
        document.getElementById("carro").style.display = 'none';        
        cleanCar();
    });
    
    btnNewCar.addEventListener('click', e=> {
        document.getElementById("carro").style.display = 'block';
    });

    // Cargar capa de información cuando cambia el select
    const vehiculo = document.getElementById("vehiculos"); 
    vehiculo.addEventListener('change', res=> {
        deleteMarkers();
//        polyLineStatus(false);
//        initMapita();
        const db = firebase.database().ref();
        const vehiculos = db.child("Vehiculos");
        
        if (vehiculo.value!="") {
            carro = vehiculos.child(vehiculo.value);
            carro.on('value', snap=> {
                document.getElementById("placa").innerHTML    = vehiculo.value;
                document.getElementById("imei").innerHTML     = snap.val().imei;
                document.getElementById("phone").innerHTML    = snap.val().telefono;
                document.getElementById("password").innerHTML = snap.val().password;
                document.getElementById("stats").innerHTML    = (snap.val().activo==1?'Activo':'Inactivo');
                document.getElementById("batery").innerHTML   = snap.val().activo;
                document.getElementById("oil").innerHTML      = snap.val().activo;
                document.getElementById("gps").innerHTML      = snap.val().activo;
                
                mostrarVehiculoMapa(snap.val().imei, loggedUser);
                
            });
            document.getElementById("comandos").className = '';
            document.getElementById("comandos").style.display = '';
            btnEditCar.style.display = 'block';
        } else {
            document.getElementById("placa").innerHTML    = "";
            document.getElementById("imei").innerHTML     = "";
            document.getElementById("phone").innerHTML    = "";
            document.getElementById("password").innerHTML = "";
            document.getElementById("stats").innerHTML    = "";
            document.getElementById("batery").innerHTML   = "";
            document.getElementById("oil").innerHTML      = "";
            document.getElementById("gps").innerHTML      = "";
            document.getElementById("comandos").className = 'hidden';
            document.getElementById("comandos").style.display = 'none';
            btnEditCar.style.display = 'none';
            
//            polyLine = [];
//            rutas = [];
//            contador = 0;
        }
        
        deleteRoutes();
    });
    
    // Salir del sistema
    btnLogout.addEventListener('click', e=> {
        firebase.auth().signOut();
        console.log("Ha salido con éxito");
        location.href="index.html";
    });
    
    var utc = new Date().toJSON().slice(0,10);
    document.getElementById("fecha_sistema").innerHTML = utc;
    document.getElementById("comandos").style.display = 'none';
    document.getElementById("carro").style.display = 'none';
    
}());

var map;
var flightPath;
var markers = [];
var polyLine = [];
function initMapita() {
    var latlng = new google.maps.LatLng(3.42319368365869, -76.5148200529943);
    map = new google.maps.Map(document.getElementById('mapa'), {
        center: latlng, // {lat: 3.42319368365869, lng: -76.5148200529943},
        zoom: 13
    });
}

function pintarRuta(from, to) {
    var directionsDisplay = new google.maps.DirectionsRenderer;
    var directionsService = new google.maps.DirectionsService;
    
    directionsDisplay.setMap(map);
    
    directionsService.route({
        origin: new google.maps.LatLng(from.lat, from.lng),
        destination: new google.maps.LatLng(to.lat, to.lng),
        travelMode: 'DRIVING'
    }, function(response, status) {
       if (status === 'OK') {
           directionsDisplay.setDirections(response);
       } else {
          console.log('Directions request failed due to ' + status);
       }
    });
    
}

function polyLineStatus(status) {
    if (status) {
        flightPath.setMap(map);
    } else {
        // Evitamos el error Cannot read property 'setMap' of undefined
        if (typeof flightPath!='undefined') {
            flightPath.setMap(null);
        }
    }
}

var rutas = [];
function paintRoute(coords) {
    console.log(coords);
    console.log("antes de ");
    var flightPlanCoordinates = coords;
    flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
    flightPath.setMap(map);
    console.log("después de ");
    
    rutas.push(flightPath);
    console.log("se agrega a rutas");
    
    // Se pinta sólo el primer y último marker
    if (coords.length>0) {
        createMarker(coords[0].lat, coords[0].lng, coords[0].imei, coords[0].time);
        createMarker(coords[coords.length-1].lat, coords[coords.length-1].lng, coords[coords.length-1].imei, coords[coords.length-1].time);
    }
//    polyLineStatus(true);
//    polyLine = [];
}

function deleteRoutes() {
    for (i=0;i<rutas.length;i++) {                           
        rutas[i].setMap(null); //or line[i].setVisible(false);
    }
    polyLine = [];
    rutas = [];
    contador = 0;
}

var infoWindow;
var contador = 0;
function mostrarVehiculoMapa(imei, idUser) {
    document.getElementById("infowindow").style.display = 'none';
    templates('infowindow');
    const db = firebase.database().ref();
    const carro = db.child("Coordenadas/"+idUser.uid+"/"+imei);
    carro.on('child_added', snap=> {
        // createMarkers(snap);
        // Se carga el array para pintar el polyLine o ruta y cada 10 registros se dibuja en el mapa
        polyLine.push(
            {
                lat: snap.val().latitud, 
                lng: snap.val().longitud, 
                time: snap.val().fecha, 
                imei: snap.val().imei 
            }
        );
        if (contador%10==0) {
            paintRoute(polyLine);
            contador = 0;
//            polyLineStatus(false);
        }
        contador++;
    });
    
    console.log("se cargó el polyline");
}

function createMarker(latitud, longitud, imei, fecha_hora) {
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(latitud, longitud),
        map: map,
        icon: "./img/car_map.png",
        // title: snap.val().imei,
    });
        
    /*
     * Se añade un evento para mostrar un infoWindow al darle 
     * click al predio
     */
    infoWindow = new google.maps.InfoWindow({
       content: 'algo'
    });
    google.maps.event.addListener(marker, 'click', function (evt) {
        var template = document.getElementById('infowindow').innerHTML;
            
        template = template.replace('#nombre#', document.getElementById("vehiculos").options[document.getElementById("vehiculos").selectedIndex].text);
        template = template.replace('#imei#', document.getElementById("imei").innerHTML);
        template = template.replace('#latitud#', latitud);
        template = template.replace('#longitud#', longitud);
        template = template.replace('#velocidad#', '');
        template = template.replace('#altitud#', '');
        template = template.replace('#gas1#', '');
        template = template.replace('#gas2#', '');
        template = template.replace('#temperatura#', '');
        template = template.replace('#gps#', '');
        template = template.replace('#acc#', '');
        template = template.replace('#door#', '');
            
        var fecha = fecha_hora;
        var ano = '20'+fecha.substr(0, 2);
        var mes = '-'+fecha.substr(2, 2);
        var dia = '-'+fecha.substr(4, 2);
        var hora = ' '+fecha.substr(6, 2);
        var min = ':'+fecha.substr(8, 2);
        var sec = ':'+fecha.substr(10, 2);
        template = template.replace('#fecha#', ano+mes+dia+hora+min+sec);
        template = template.replace('#millas#', '');
           
        infoWindow.setContent(template);
        infoWindow.open(map, marker);
        infoWindow.setPosition(evt.latLng);
    });
        
    markers.push(marker);
}

function createMarkers2(snap) {
        var marker = new google.maps.Marker({
             position: new google.maps.LatLng(snap.val().latitud, snap.val().longitud),
             map: map,
             icon: "./img/car_map.png",
             // title: snap.val().imei,
        });
        
        /*
         * Se añade un evento para mostrar un infoWindow al darle 
         * click al predio
         */
        infoWindow = new google.maps.InfoWindow({
            content: 'algo'
        });
        google.maps.event.addListener(marker, 'click', function (evt) {
            var template = document.getElementById('infowindow').innerHTML;
            
            template = template.replace('#nombre#', document.getElementById("vehiculos").options[document.getElementById("vehiculos").selectedIndex].text);
            template = template.replace('#imei#', document.getElementById("imei").innerHTML);
            template = template.replace('#latitud#', snap.val().latitud);
            template = template.replace('#longitud#', snap.val().longitud);
            template = template.replace('#velocidad#', '');
            template = template.replace('#altitud#', '');
            template = template.replace('#gas1#', '');
            template = template.replace('#gas2#', '');
            template = template.replace('#temperatura#', '');
            template = template.replace('#gps#', '');
            template = template.replace('#acc#', '');
            template = template.replace('#door#', '');
            
            var fecha = snap.val().fecha;
            var ano = '20'+fecha.substr(0, 2);
            var mes = '-'+fecha.substr(2, 2);
            var dia = '-'+fecha.substr(4, 2);
            var hora = ' '+fecha.substr(6, 2);
            var min = ':'+fecha.substr(8, 2);
            var sec = ':'+fecha.substr(10, 2);
            template = template.replace('#fecha#', ano+mes+dia+hora+min+sec);
            template = template.replace('#millas#', '');
            
            infoWindow.setContent(template);
            infoWindow.open(map, marker);
            infoWindow.setPosition(evt.latLng);
        });
        
        markers.push(marker);
}

function deleteMarkers() {
    //Loop through all the markers and remove
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
}

function cleanCar() {
    document.getElementById('carro').style.display = 'none';
    document.getElementById("txtCarroNombre").value = '';
    document.getElementById("txtCarroPlaca").value = '';
    document.getElementById("txtCarroPlaca").readOnly = false;
    document.getElementById("txtCarroIMEI").value = '';
    document.getElementById("txtCarroIMEI").readOnly = false;
    document.getElementById("txtCarroTelefono").value = '';
    document.getElementById("txtCarroPassword").value = '';
}

var template = "";
function templates(nombre) {
    var xmlhttp;
    if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp = new XMLHttpRequest();
    } else { // code for IE6, IE5
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById(nombre).innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("GET", "templates/"+nombre+".html", true);
    xmlhttp.send();
}

function sendCommand(phone, placa, password, command) {
    // Si el parámetro phone está vacio, fue porque lo enviaron desde el panel de comandos
    if (phone=="") {
        phone = document.getElementById("phone").innerHTML;
        placa = document.getElementById("placa").innerHTML;
        password = document.getElementById("password").innerHTML;
    }
    
    var http = new XMLHttpRequest();
    var url = "http://cgclab.co/gpstracker/commands.php";
    var params = "comando="+command+"&phone="+phone+"&placa="+placa+"&password="+password;
    http.open('POST', url, true);

    //Send the proper header information along with the request
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

    http.onreadystatechange = function() {//Call a function when the state changes.
        if(http.readyState == 4 && http.status == 200) {
            console.log(http.responseText);
            
            var json = JSON.parse(http.responseText);
            if (json.success==1) {
                alert(json.data);
            } else {
                console.log(json.data);
            }
        }
    }
    http.send(params);
}

function cargarSpinner(userID) {
    var carros = document.getElementById("vehiculos");
    const db = firebase.database().ref();
    const vehiculos = db.child("Vehiculos");
    
    const query = vehiculos.orderByChild("idUsuario").equalTo(userID);
    
    query.on('child_added', snap=>{
        var carro = document.createElement('option');
        carro.value = snap.key;
        carro.innerHTML = snap.val().nombre;
        carros.appendChild(carro);
    });    
    
}


//initMap();     
var navegador = navigator.userAgent;
var ese;
var caliPolygon = new Array();
var constPolygon = new Array();
var lineaAmobPolygon = new Array()
var poliAmobPolygon = new Array()
var puntoAmobMarkers = [];
var markerLogos = [];
var markerLogo = new Array();
var markerCluster;
var map;
var marker;
var geocoder;
var dataIni = {
    zoom: 17,
    center: {
        lat: 3.42319368365869,
        lng: -76.5148200529943
    }
};
/*    var infoWindow = new google.maps.InfoWindow({
        content: ''
    });
    /**
     * Inicializa el objeto de Google Maps, cargando las coordenadas de los poligonos;
     * se muestra un infoWindow para la informaciÃ³n general del predio
     */
    function initMap() {
        console.log("entro");
        map = new google.maps.Map(document.getElementById('mapa'), {
          center: {lat: 3.42319368365869, lng: -76.5148200529943},
          zoom: 13
        });

        
        
        //definimos que los comercios tengan visibilidad "off"
        var styles = [
                {
                  featureType: "poi.business",
                  elementType: "labels",
                  stylers: [
                    { visibility: "off" }
                  ]
                }
              ];
     
        //creamos un objeto styledMap utilizando la definicion anterior
        var styledMap = new google.maps.StyledMapType(styles, {name: "Styled Map"});          
        map = new google.maps.Map(document.getElementById('map'), dataIni);
        
        //Asociamos los estilos al mapa.... y listo!
        map.mapTypes.set('map_style', styledMap);
        map.setMapTypeId('map_style');

        // Cuando el zoom cambie, se debe reiniciar el marker clusterer, sino las imÃ¡genes aparecerÃ¡n
    //    google.maps.event.addListener(map, 'zoom_changed', function(){
    //        markerCluster = new MarkerClusterer(map, markerLogos, {imagePath: 'mod/Bienes/img/images/m'});
    //    });

    }
    