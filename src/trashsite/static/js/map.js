//code edited by william

var map;
var monsterArray = [];
var shapes = [];
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
  //for (let i= 0; i < markers.length; i++) {
  //  monsterArray[i].marker.setMap(null);
  //  shapes[i].setMap(null);
  //}
  //shapes=[];
  //markers=[];
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
    monsterArray.push({"id":element.TM_ID,"monster":element,"marker":marker})
    
    drawShape(element);

    marker.addListener("click", () => {
      //temporary fix for events triggering multiple times when clicking on the markers. Will only be able to press once in final code
      var oldButton = document.getElementById("enterScore");
      var button = oldButton.cloneNode(true);
      oldButton.parentNode.replaceChild(button,oldButton);

      monsterArray.forEach(element => {
        if(element.marker==marker){
          let monster = element.monster;
          document.getElementById("showPoints").textContent="Red Team Points:"+monster.Team1_Score+"Green Team Points:"+monster.Team2_Score+"Blue Team Points"+ monster.Team3_Score
          console.log("you have clicked on marker with id: "+element.id);
          
          //bit of a jank system, button press is done here instead of the usual onclick="" stuff
          button.addEventListener("click", async () => {
            var scoreInc=[0,0,0];
            let value = document.querySelector('input[name="points"]:checked').value;
            switch(value){
              case "red_team":scoreInc[0]++;break;
              case "green_team":scoreInc[1]++;break;
              case "blue_team":scoreInc[2]++;break;
            }
            updateScore(monster.TM_ID,scoreInc).then(response =>{
              element.monster = response;
              monster = response;
              document.getElementById("showPoints").textContent="Red Team Points:"+monster.Team1_Score+"Green Team Points:"+monster.Team2_Score+"Blue Team Points"+ monster.Team3_Score
              //drawMonsters();
            })
          })
        }
      });
    });
  });
}

function drawShape(monster){
  var circleColour = "#000000";
  var radius;
  if(monster.Team1_Score>monster.Team2_Score && monster.Team1_Score>monster.Team2_Score){
    circleColour="#FF0000";
    if(monster.Team2_Score>monster.Team3_Score){
      radius=monster.Team1_Score-monster.Team2_Score;
    }
    else{
      radius=monster.Team1_Score-monster.Team3_Score;
    }
  }
  else if(monster.Team2_Score>monster.Team1_Score && monster.Team2_Score>monster.Team3_Score){
    circleColour="#00ff00";
    if(monster.Team1_Score>monster.Team3_Score){
      radius=monster.Team2_Score-monster.Team1_Score;
    }
    else{
      radius=monster.Team2_Score-monster.Team3_Score;
    }
  }
  else if(monster.Team3_Score>monster.Team1_Score && monster.Team3_Score>monster.Team2_Score){
    circleColour="#0000ff";
    if(monster.Team1_Score>monster.Team2_Score){
      radius=monster.Team3_Score-monster.Team1_Score;
    }
    else{
      radius=monster.Team3_Score-monster.Team2_Score;
    }
  }
  else{radius=0};
  console.log(circleColour);
  var shape = new google.maps.Circle({
    map:map,
    fillColor:circleColour,
    center:{lat:monster.Latitude,lng:monster.Longitude},
    radius:radius*5});
    shapes.push(shape);
}

function createMonster(){ //there will be a button to press instead at later date
  const monster = {"Latitude":50.73646948193597,"Longitude":-3.5317420013942633};
  const url="api/monsters/add-tm";
  const params = {body:JSON.stringify(monster),method:"POST",headers: {"content-type":"application/json"}};
  fetch(url,params).then(async function(response){
    if(response.ok){
      //return response.json()
      console.log(await response.json());
    }
    else {throw new Error("very sad didnt work :(" + response.statusText)}
  });
}

async function updateScore(id,scores){
  const data = {"TM_ID":id,"T1Score":scores[0],"T2Score":scores[1],"T3Score":scores[2]};
  const url="api/monsters/add-score";
  const params = {body:JSON.stringify(data),method:"POST",headers: {"content-type":"application/json"}};
  return fetch(url,params).then(response => response.json());
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
  //console.log("latitude:"+latitude+" longitude:"+longitude);
  //map.panTo({lat:latitude,lng:longitude});
}
function success(position){ //will handle distances from monsters to player
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  //console.log("latitude:"+latitude+" longitude:"+longitude);
  //map.panTo({lat:latitude,lng:longitude});
}
function failure(){
  return [50.73646948193597, -3.5317420013942633]
}

window.initMap = initMap;