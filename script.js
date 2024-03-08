//Gets Google Maps APi Key
import config from '../config.js';
let map;
let customPopup;
let markersData;
function Load_Map(){
  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}
async function initMap() {
  const { Map, Marker, InfoWindow } = await google.maps.importLibrary("maps");

  //creates map instance, map centered on chesapeake bay
  map = new Map(document.getElementById("map"), {
    center: { lat: 38.5, lng: -76.5 },
    zoom: 8,
  });


  /* Add markers to the map
  array markersData that sets position(lng & lat) and the marker title */
  markersData = [
    { position: { lat: 38.581805, lng: -77.268023 }, title: "Powells Creek", description: "this is fake data", graph: "images/powellcreek1.png"},
    { position: { lat: 38.14749, lng: -76.98545 }, title: "walnut hill", description: "this is fake data", graph: "images/walnutHill2.png"},
    { position: { lat: 37.17166667, lng: -76.70638889}, title: "Surry Power Station", description: "Source type: Surface Water Intake", graph: "images/Surry_Power_Station.png" },
    { position: { lat: 38.063056, lng: -77.790556}, title: "NORTH ANNA NUCLEAR POWER PLANT", description: "Source type: Surface Water Intake", graph: "images/NorthAnnaNuclearPlant.png"},
    // Add more markers as needed
  ];

  /* iterates through each marker and places position on map
  (markersInfo => takes data from markersData and puts them into markersInfo */
  markersData.forEach(markerInfo => {
    const marker = new google.maps.Marker({ 
      position: markerInfo.position, 
      map: map,
      title: markerInfo.title,
      description: markerInfo.description, 
      graph: markerInfo.graph,
    });
    
    //infowindow for hover
    const infowindow = new InfoWindow({
      content: `
      <div class = "info-window">
      <strong>${markerInfo.title}</strong>
      </div>
      `,
      maxWidth: 300,
    });
    //action for mouse hovering
    marker.addListener('mouseover', () => {
      infowindow.open(map, marker);
    });

    marker.addListener('mouseout', () => {
      infowindow.close();
    });
    //adds interactive function to marker on click
    marker.addListener("click", () => {
      openPopup(marker);
    });
  });
}

//function finds id="popup" then sets HTML content inside the element with id="popup"
function openPopup(marker) {
  customPopup = document.getElementById('popup');
  customPopup.innerHTML = `
    <h1>${marker.getTitle()}</h1>
    <div class="info-window">
      <p>Latitude: ${marker.getPosition().lat()}   Longitude: ${marker.getPosition().lng()} </p>
      <button id="graph-button" onclick="switchGraph('${marker.graph}')">Graphs</button>
      <img id="img-graph" src="${marker.graph}" alt="graph" style="width:400px;height:370px;">
      <p>${marker.description}</p>
      <div id="close-button" onclick="closePopup()">X</div>
    </div>
    
  `;
  customPopup.style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
}

function closePopup() {
  customPopup = document.getElementById('popup');
  customPopup.style.display = 'none';
  document.getElementById('overlay').style.display = 'none';
}

//fucntion to handle button graph
function switchGraph(currentGraph) {
  const imgGraph = document.getElementById('img-graph');
  
  if (currentGraph === 'images/Surry_Power_Station.png') {
    imgGraph.src = 'images/linegraph1.png';
  } 
  if(currentGraph === 'images/NorthAnnaNuclearPlant.png'){
    imgGraph.src = 'images/linegraph2.png';
  }
  if(currentGraph === 'images/linegraph1.png'){
    imgGraph.src = 'images/Surry_Power_Station.png';
  }
  if(currentGraph === 'images/linegraph2.png'){
    imgGraph.src = 'images/NorthAnnaNuclearPlant.png';
  }
  if (currentGraph === 'images/powellcreek1.png') {
    imgGraph.src = 'images/powellcreek2.png';
  } 
  if(currentGraph === 'images/powellcreek12.png'){
    imgGraph.src = 'images/powellcreek1.png';
  }
  if(currentGraph === 'images/walnutHill2.png'){
    imgGraph.src = 'images/walnutHill1.png';
  }
  if(currentGraph === 'images/walnutHill1.png'){
    imgGraph.src = 'images/walnutHill2.png';
  }
  
}
window.switchGraph = switchGraph;

//makes functions globally available
window.openPopup = openPopup;
window.closePopup = closePopup;

//search function doesnt work???
function search() {
  //searchs HTML for element id "search-input" sets user input to lowercase
  const searchInput = document.getElementById("search-input").value.toLowerCase();

  //console.log("Marker title: ", markerInfo.getTitle);
  //iterates through each marker, sets lowercase, then finds match with searchInput
  marker.forEach(markerInfo => {
      const markerTitle = markerInfo.title.toLowerCase();

      if (markerTitle.includes(searchInput)) {
          console.log("Match found!");
          openPopup(marker);
      } else {
        console.log("not found");
      }
  });

}
document.getElementById("search-button").addEventListener("click", search);

window.search = search;
//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
