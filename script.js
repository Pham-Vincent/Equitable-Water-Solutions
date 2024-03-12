//Gets Google Maps APi Key
import config from '../config.js';
let map;
let customPopup;
let markersData;
let markers = []; //stores markers used in search()

function Load_Map(){
  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"places");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}

//object to store sets of images
const imageSets = {
  'images/Surry_Power_Station.png': ['images/linegraph1.png', 'images/Surry_Power_Station.png'],
  'images/NorthAnnaNuclearPlant.png': ['images/linegraph2.png', 'images/NorthAnnaNuclearPlant.png'],
  'images/powellcreek1.png': ['images/powellcreek2.png', 'images/powellcreek1.png'],
  'images/walnutHill2.png': ['images/walnutHill1.png', 'images/walnutHill2.png']
};

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
    { position: { lat: 38.581805, lng: -77.268023 }, title: "Powells Creek", description: "this is fake data", graph: "images/powellcreek1.png", state: "Prince William, VA"},
    { position: { lat: 38.14749, lng: -76.98545 }, title: "walnut hill", description: "this is fake data", graph: "images/walnutHill2.png", state:"Westmoreland, VA"},
    { position: { lat: 37.17166667, lng: -76.70638889}, title: "Surry Power Station", description: "Source type: Surface Water Intake", graph: "images/Surry_Power_Station.png", state: "Surry, VA"},
    { position: { lat: 38.063056, lng: -77.790556}, title: "NORTH ANNA NUCLEAR POWER PLANT", description: "Source type: Surface Water Intake", graph: "images/NorthAnnaNuclearPlant.png", state:"Louisa, VA"},
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
      state: markerInfo.state,
    }); 


    //adds marker to array, used in search()
    markers.push(marker);
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
      popUpLayer1(marker);
    });
  });

  const input = document.getElementById("search-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_CENTER].push(input);
}

//first layer popup
function popUpLayer1(marker){
  //Close the currently open info window, if any
  if (window.smallInfowindow) {
    window.smallInfowindow.close();
  }
  const smallInfowindow = new google.maps.InfoWindow({
    content: `
      <div class="info-window">
        <strong>${marker.getTitle()}</strong>
        <p>${marker.state}</p>
        <p>${marker.description}</p>
        <button id="view-more-button" onclick="viewMore('${marker.graph}')">View More</button>
      </div>
    `,
    maxWidth: 300,
  });
  
  smallInfowindow.open(map, marker);
  window.currentMarker = marker;
  window.smallInfowindow = smallInfowindow;
  
}
//Function to handle the view more button
function viewMore(currentGraph) {
  window.smallInfowindow.close();
  openPopup(window.currentMarker, currentGraph);
}
//function finds id="popup" then sets HTML content inside the element with id="popup"
function openPopup(marker, currentGraph) {
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

//closes popup upon clicking overlay
document.getElementById('overlay').addEventListener('click', closePopup);

//fucntion to handle graph button
function switchGraph(currentGraph) {
  const imgGraph = document.getElementById('img-graph');
  //Check if the currentGraph is in the imageSets object then toggle between images in the set
  if (imageSets.hasOwnProperty(currentGraph)) {
    const imageSet = imageSets[currentGraph];
    imgGraph.src = (imgGraph.src.includes(imageSet[0])) ? imageSet[1] : imageSet[0];
  }
}

//makes functions globally available
window.switchGraph = switchGraph;
window.openPopup = openPopup;
window.closePopup = closePopup;
window.popUpLayer1 = popUpLayer1;
window.viewMore = viewMore;

//handles enter key for search()
function handleKeyPress(event) {
  if (event.keyCode === 13) {
    const searchInput = document.getElementById("search-input").value.trim();
    if (searchInput !== "") {
      search();
    }
  }
}


function search() {
  //Search HTML for element id "search-input" and set user input to lowercase
  const searchInput = document.getElementById("search-input").value.toLowerCase();

  //Iterate through each marker
  markers.forEach(marker => {
    const markerTitle = marker.getTitle().toLowerCase();

    if (markerTitle.includes(searchInput)) {
      console.log("Match found!");
      openPopup(marker, marker.graph);
    } else {
      console.log("Not found");
    }
  });
}
//event listener for search enter press
document.getElementById("search-input").addEventListener("keypress", handleKeyPress);

window.search = search;
//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
