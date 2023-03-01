//code edited by william

var map;
var monsterArray = [];
var shapes = [];
var curLocation = false;
var zoomedIn = true;

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
    console.log("hi");
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

  map.addListener("click",(event) => {
    let latLng = event.latLng;
    var clickLat = latLng.lat();
    var clickLng = latLng.lng();
    document.getElementById("latitude").value=clickLat;
    document.getElementById("longitude").value=clickLng;
  })
  //will track position


  navigator.geolocation.watchPosition(successMove,failure,{timeout:5000});

  getMonsters().then(response => {
    if(response!=null){
    response.forEach(element => {
      drawMonsters(element);
    });
  }
  })
  setInterval(test,2400);
}


function test(){
  getMonsters().then(response => {
    if(response!=null){
    response.forEach(element => {
      drawMonsters(element);
    });
  }
  })
}
async function getMonsters(){
  const url="api/monsters/get-tms";
  const response = await fetch(url, { method: "get" });
    return await response.json();
}

async function setMonster(latitude,longitude){
  const monster = {"Latitude":latitude,"Longitude":longitude};
    const url="api/monsters/add-tm";
    var csrftoken = Cookies.get('csrftoken');
    const params = {
      credentials: 'include',
      body:JSON.stringify(monster),
      method:"POST",
      headers: {"X-CSRFToken": csrftoken,"content-type":"application/json"}};
    return fetch(url,params).then(response => response.json());
}

function drawMonsters(monster){
  var done = false;
  monsterArray.forEach(element => {
    if(monster.TM_ID==element.monster.TM_ID){
      element.monster=monster;
      done = true;
      if(getRadius(monster).radius!=element.shape.getRadius()/5){
        var newShape = drawShape(monster);
        element.shape.setMap(null);
        element.shape = newShape;
      }
      return;
      }
    })
  if(!done){
    let latitude = monster.Latitude;
    let longitude = monster.Longitude;
    var marker = new google.maps.Marker({
      position:{lat:latitude,lng:longitude},
      map,
      //title:"id:"+monster.TM_ID,
    })
    var shape = drawShape(monster);
    monsterArray.push({"id":monster.TM_ID,"monster":monster,"marker":marker,"shape":shape})

    marker.addListener("click", () => {
      //temporary fix for events triggering multiple times when clicking on the markers. Will only be able to press once in final code
      var oldButton = document.getElementById("enterScore");
      var button = oldButton.cloneNode(true);
      oldButton.parentNode.replaceChild(button,oldButton);

      monsterArray.forEach(element => {
        if(element.marker==marker){
          let monster = element.monster;
          document.getElementById("status").textContent="Red Team Points:"+monster.Team1_Score+" Green Team Points:"+monster.Team2_Score+" Blue Team Points:"+ monster.Team3_Score
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
              document.getElementById("status").textContent=" Red Team Points:"+monster.Team1_Score+" Green Team Points:"+monster.Team2_Score+" Blue Team Points:"+ monster.Team3_Score
              drawMonsters(monster);
            })
          })
        }
      });
    });
  }
}

function getRadius(monster){
  var colour = "#000000";
  var radius;
  if(monster.Team1_Score>monster.Team2_Score && monster.Team1_Score>monster.Team3_Score){
    colour="#FF0000";
    if(monster.Team2_Score>monster.Team3_Score){
      radius=monster.Team1_Score-monster.Team2_Score;
    }
    else{
      radius=monster.Team1_Score-monster.Team3_Score;
    }
  }
  else if(monster.Team2_Score>monster.Team1_Score && monster.Team2_Score>monster.Team3_Score){
    colour="#00ff00";
    if(monster.Team1_Score>monster.Team3_Score){
      radius=monster.Team2_Score-monster.Team1_Score;
    }
    else{
      radius=monster.Team2_Score-monster.Team3_Score;
    }
  }
  else if(monster.Team3_Score>monster.Team1_Score && monster.Team3_Score>monster.Team2_Score){
    colour="#0000ff";
    if(monster.Team1_Score>monster.Team2_Score){
      radius=monster.Team3_Score-monster.Team1_Score;
    }
    else{
      radius=monster.Team3_Score-monster.Team2_Score;
    }
  }
  else{radius=0};
  return {"colour": colour,"radius":radius};
}

function drawShape(monster){
  let data = getRadius(monster);
  circleColour=data.colour;
  radius=data.radius;
  var shape = new google.maps.Circle({
    map:map,
    fillColor:circleColour,
    center:{lat:monster.Latitude,lng:monster.Longitude},
    radius:radius*5});
  return shape;
}


function createMonster(){ //there will be a button to press instead at later date
  let latitude = document.getElementById("latitude").value
  let longitude = document.getElementById("longitude").value
  document.getElementById("status").textContent="New monster created!"
  if(latitude == null || longitude == null){
    console.log("invalid input");
  }
  else{
    setMonster(latitude,longitude).then(response => {
      drawMonsters(response);
    })
  }
  
}


async function updateScore(id,scores){
  const data = {"TM_ID":id,"T1Score":scores[0],"T2Score":scores[1],"T3Score":scores[2]};
  const url="api/monsters/add-score";
  var csrftoken = Cookies.get('csrftoken');
  const params = {credentials: 'include',body:JSON.stringify(data),method:"POST",headers: {"X-CSRFToken": csrftoken,"content-type":"application/json"}};
  return fetch(url,params).then(response => response.json());
}

function toggleLocation(){
  if(curLocation==false) {
    curLocation = true;
    console.log("enabled");  
  }
  else if(curLocation==true) curLocation = false;
}

function changeZoom() {
  if(zoomedIn){
      if(map.getZoom()>15){
          
          google.maps.event.addListenerOnce(map, 'zoom_changed', function(event) {
          changeZoom();
      });
      setTimeout(function(){map.setZoom(map.getZoom()-1)},80);
      }
      else{
          zoomedIn=false;
      }
  }
  else{
      if(map.getZoom()<18){
          google.maps.event.addListenerOnce(map, 'zoom_changed', function(event) {
              changeZoom();
          });
          setTimeout(function(){map.setZoom(map.getZoom()+1)},80);
      }
      else{
          zoomedIn=true;
      }
  }
}



function successMove(position){ //will handle distances from monsters to player
  console.log(curLocation);
  var latitude = position.coords.latitude;
  var longitude = position.coords.longitude;
  if(curLocation==true){
    console.log(latitude,longitude);
    map.panTo({lat:latitude,lng:longitude});
  }
  else{
    map.panTo({lat:50.73646948193597,lng:-3.5317420013942633})
  }
}
function success(position){ //will handle distances from monsters to player
  return position.coords
}
function failure(){
  return [50.73646948193597, -3.5317420013942633]
}

window.initMap = initMap;