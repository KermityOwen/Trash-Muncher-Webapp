//code edited by william

var map;
//draws the map onto the screen
function initMap(){
//future code for setting current position
var geoButton = document.getElementById("geoButton");
var coords;
navigator.permissions.query({name:'geolocation'}).then(async (result) => {
  if(result.state === 'granted'){
    geoButton.style.display = 'none';
    await getPosition();
    
  }
  else if(result.state==='prompt'){
    geoButton.style.display = 'none';
    coords = navigator.geolocation.getCurrentPosition(success,failure);}
  else if(result.state==='denied'){
    geoButton.style.display = 'inline';
  }
  result.addEventListener('change', async () => {
    if(result.state==='granted'){
      await getPosition();
    }
    if(result.state==='denied'){
      geoButton.style.display = 'inline';
    }
  });
});

//future code to draw shapes for the area of control

}

async function getPosition(){
  return new Promise((resolve,reject) => {
    navigator.geolocation.getCurrentPosition(position => {resolve(createMap(position.coords))},reject);
  });
}


function createMap(coords){
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 18,
    tilt:45,
    disableDefaultUI: true,
    zoomControl: false,
    gestureHandling: "none",
    center: {lat: coords.latitude, lng: coords.longitude},
    mapId:'805b0b106a1a291d'
  });

  //gets the monsters to put on the map
  const http = new XMLHttpRequest();
  const url="api/monsters/get-tms";
  http.open("GET",url);
  http.send();

  http.onreadystatechange = (e) => {
    if (http.readyState === XMLHttpRequest.DONE) {
      const monsters=JSON.parse(http.responseText);
      drawMonsters(monsters);
    }
  }
}

function runPermission(){
  alert("hi");
  navigator.geolocation.getCurrentPosition(success,failure);
}

function drawMonsters(monsters){
  console.log(monsters);
  monsters.forEach(element => {
    let latitude = element.Latitude;
    let longitude = element.Longitude;

    //currently only creates a google map marker, will create a 3d object at a later date which can store id, this cannot.
    new google.maps.Marker({
      position:{lat:latitude,lng:longitude},
      map,
      title:"id:"+element.TM_ID,
    })
    console.log("latitude:"+latitude+" longitude:"+longitude);
  });
}

function createMonster(){
  const http = new XMLHttpRequest();
  const url="api/monsters/add-tm";
  const monster = {"Latitude":50.73646948193597,"Longitude":-3.5317420013942633};
  //const monster = {"TM_ID":0, "T1Score":1, "T2Score":2, "T3Score":4};
  http.open("POST",url);
  http.setRequestHeader("Accept", "application/json");
  http.setRequestHeader("Content-Type", "application/json");
  http.send(JSON.stringify(monster));

  http.onreadystatechange = (e) => {
    if (http.readyState === XMLHttpRequest.DONE) {
      console.log(http.status);
      console.log(http.responseText);
    }
  }
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


function success(position){
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  var coords=[longitude,latitude];
  return coords;
}

function failure(){
  return [50.73646948193597, -3.5317420013942633]
}

window.initMap = initMap;