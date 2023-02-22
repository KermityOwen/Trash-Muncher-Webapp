//code edited by william

var map;
//draws the map onto the screen
function initMap(){
//future code for setting current position


map = new google.maps.Map(document.getElementById("map"), {
        zoom: 18,
        tilt:45,
        disableDefaultUI: true,
        zoomControl: false,
        gestureHandling: "none",
        center: {lat: 50.73646948193597, lng: -3.5317420013942633},
        mapId:'805b0b106a1a291d'
      });
//future code to draw shapes for the area of control

}

//will be called on a click event with the gmaps api, passes in longitude, latitude
function placeMonster(){
  //creates a form to add a monster to the map
  if(document.getElementById("form")){

  }
  else{
  alert("cool monster button");
  const form = document.createElement("div");
  form.id="form";
  const button = document.createElement("button");
  button.textContent="button";
  form.append(button);
  document.body.append(form);
  }
}
window.initMap = initMap;