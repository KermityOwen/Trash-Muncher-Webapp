function sendLocation() {
  var name = document.getElementById("location_name");
  var radio = document.querySelector('input[name="location_size"]:checked').value;

  alert(name.value);
  alert(radio);

  return false;
}

function initMap(){
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    tilt:45,
    disableDefaultUI: true,
    center: {lat: 50.73646948193597, lng: -3.5317420013942633},
    mapId:'805b0b106a1a291d'
  });

}