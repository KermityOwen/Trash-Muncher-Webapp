var map;
function initMap(){
map = new google.maps.Map(document.getElementById("map"), {
        zoom: 18,
        tilt:45,
        disableDefaultUI: true,
        zoomControl: false,
        gestureHandling: "none",
        center: {lat: 50.73646948193597, lng: -3.5317420013942633},
        mapId:'805b0b106a1a291d'
      });
}
window.initMap = initMap;