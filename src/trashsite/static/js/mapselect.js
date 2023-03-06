var map;
var monsterArray = [];
var shapes = [];
var curLocation = false;
var zoomedIn = true;


function sendLocation() {
  var name = document.getElementById("location_name");
  var radio = document.querySelector('input[name="location_size"]:checked').value;

  alert(name.value);
  alert(radio);

  return false;
}

function initMap(){
  map = new google.maps.Map(document.getElementById("map"), options.gamekeeper);

  //only gamekeeper
  map.addListener("click",(event) => {
    let latLng = event.latLng;
    var clickLat = latLng.lat();
    var clickLng = latLng.lng();
    document.getElementById("latitude").value=clickLat;
    document.getElementById("longitude").value=clickLng;
  })

  //all users
  getMonsters().then(response => {
    if(response!=null){
    response.forEach(element => {
      drawMonsters(element);
    });
  }
  })
  setInterval(test,2400);

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
          
          //bit of a jank system, button press is done here instead of the usual onclick="" stuff
          //this can hopefully be fixed with svelte, ugly right now but better implementation with it
          button.addEventListener("click", async () => {
            //TODO - allow both individual score increases/decreases and completely changing the scores
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

async function getMonsters(){
  const url="api/monsters/get-tms";
  const response = await fetch(url, { method: "get" });
    return await response.json();
}

window.initMap = initMap;