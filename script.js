//Gets Google Maps APi Key
import config from '../config.js';
let map;
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
  const markersData = [
    { position: { lat: 38.581805, lng: -77.268023 }, title: "Powells Creek" },
    { position: { lat: 38.363350, lng: -75.605919 }, title: "Salisbury" },
    { position: { lat: 38.14749, lng: -76.98545 }, title: "walnut hill" },
    // Add more markers as needed
  ];

  /* iterates through each marker and places position on map
  (markersInfo => takes data from markersData and puts them into markersInfo */
  markersData.forEach(markerInfo => {
    const marker = new google.maps.Marker({ 
      position: markerInfo.position, 
      map: map,
      title: markerInfo.title,
    });
   
    /* creates info window instance 
    <div> - groups text
    <strong> - boldens title text
    <p> - sets paragraph */
    const infowindow = new InfoWindow({
      content: `
      <div class = "info-window">
      <strong>${markerInfo.title}</strong>
      <p>The vibrant cityscape illuminated by neon lights creates a captivating atmosphere in the bustling metropolis. As people navigate the busy streets, the aroma of diverse cuisines wafts through the air, enticing passersby. In the heart of the city, iconic landmarks stand tall, weaving together a rich tapestry of history and modernity.</p>
      </div>
      `,
      maxWidth: 300,
    });

    //adds interactive function to marker on click
    marker.addListener("click", () => {
      infowindow.open(map, marker);
    });
  });
}

//search function doesnt work

function search() {
  //searchs HTML for element id "search-input" sets user input to lowercase
  const searchInput = document.getElementById("search-input").value.toLowerCase();

  //iterates through each marker, sets lowercase, then finds match with searchInput
  markers.forEach(marker => {
      const markerTitle = marker.getTitle().toLowerCase();

      if (markerTitle.includes(searchInput)) {
          marker.setIcon(getColoredMarkerIcon('blue'));
          marker.setMap(map);
      } else {
          marker.setMap(null);
      }
  });

  document.getElementById("search-button").addEventListener("click", search);
}

//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
