//code edited by william

var map;
var monsterArray = [];
//draws the map onto the screen
function initMap(){
//future code for setting current position
var coords;
navigator.permissions.query({name:'geolocation'}).then(async (result) => {
  if(result.state === 'granted'){
    await getPosition();
    
  }
  else if(result.state==='prompt'){
    await getPosition();
  }
  else if(result.state==='denied'){
    geoButton.style.display = 'inline';
  }
  result.addEventListener('change', async () => {
    if(result.state==='granted'){
      await getPosition();
    }
    if(result.state==='denied'){
    }
  });
});

//future code to draw shapes for the area of control

}
//deals with initial current position
async function getPosition(){
  return new Promise((resolve,reject) => {
    navigator.geolocation.getCurrentPosition(position => {resolve(createMap(position.coords))},reject);
  });
}

//def important function needs changing for different uses
function createMap(coords){
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 18,
    tilt:45,
    disableDefaultUI: true,
    zoomControl: false,
    gestureHandling: "none",
    center:{lat: 50.73646948193597,lng: -3.5317420013942633},
    //center: {lat: coords.latitude, lng: coords.longitude},
    mapId:'805b0b106a1a291d'
  });
  //const webglOverlayView = new google.maps.WebGLOverlayView();
  //webglOverlayView.setMap(map);

  navigator.geolocation.watchPosition(successMove);

  //gets the monsters to put on the map
  const url="api/monsters/get-tms";
  fetch(url,{method:"get"}).then(async function(response){
    if(response.ok){
      drawMonsters(await response.json())
      console.log(monsterArray);
    }
    else {throw new Error("very sad didnt work :(" + response.statusText)}
  })
}


function drawMonsters(monsters){
  console.log(monsters);
  monsters.forEach(element => {
    
    let latitude = element.Latitude;
    let longitude = element.Longitude;

    //currently only creates a google map marker, will create a 3d object at a later date which can store id, this cannot.
    console.log("creating a marker");
    var marker = new google.maps.Marker({
      position:{lat:latitude,lng:longitude},
      map,
      title:"id:"+element.TM_ID,
    })
    marker.addListener("click", () => {
      console.log("hi there im cool");
    });
    monsterArray.push([element.TM_ID,marker])
    console.log("latitude:"+latitude+" longitude:"+longitude);
  });
}

function createMonster(){
  const monster = {"Latitude":50.73646948193597,"Longitude":-3.5317420013942633};
  const url="api/monsters/add-tm";
  const params = {body:JSON.stringify(monster),method:"POST",headers: {"content-type":"application/json"}}
  fetch(url,params).then(async function(response){
    if(response.ok){
      //return response.json()
      console.log(await response.json());
    }
    else {throw new Error("very sad didnt work :(" + response.statusText)}
  });
}

//mostly a test thing, dont think its going to be used

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


function successMove(position){ //will handle distances from monsters to player
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  console.log("latitude:"+latitude+" longitude:"+longitude);
  //map.panTo({lat:latitude,lng:longitude});
}
function success(position){ //will handle distances from monsters to player
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  console.log("latitude:"+latitude+" longitude:"+longitude);
  //map.panTo({lat:latitude,lng:longitude});
}
function failure(){
  return [50.73646948193597, -3.5317420013942633]
}

window.initMap = initMap;