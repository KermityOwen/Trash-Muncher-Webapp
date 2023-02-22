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
function placeMonster(){ //need to add parameters once working
  //creates a form to add a monster to the map
  if(document.getElementById("form")){

  }
  else{
    const form = document.createElement("form");
    form.action="/map";
    form.id="form";
    form.method="post";

    const label = document.createElement("label");
    label.for="lat";
    label.textContent="Latitude";
    form.append(label);
    const lat = document.createElement("input");
    lat.name="lat";
    lat.id = "lat";
    lat.value=50.73646948193597;
    lat.readOnly = true;
    form.append(lat);
    form.append(document.createElement("br"));

    const label2 = document.createElement("label");
    label2.for="lng";
    label2.textContent="Longitude";
    form.append(label2);
    const lng = document.createElement("input");
    lng.name="lat";
    lng.value=-3.5317420013942633;
    lng.readOnly = true;
    form.append(lng);
    form.append(document.createElement("br"));

    const button = document.createElement("input");
    button.type="submit";
    button.value="Submit";
    form.append(button);
    document.body.append(form);
  }
}

function ajax(){
  alert("this will do ajax shit soon");
}
window.initMap = initMap;