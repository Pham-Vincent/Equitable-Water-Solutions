//Gets Google Maps APi Key
import config from './config.js';
import { popUpLayer1, openPopup, closePopup, viewMore } from './popup.js';
import { search } from './search.js';
let map;
let markers = []; //stores markers used in search()


function Load_Map(){
  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"places");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}

async function initMap() {
  const { Map, Marker, InfoWindow } = await google.maps.importLibrary("maps");

  //creates map instance, map centered on chesapeake bay
  map = new Map(document.getElementById("map"), {
    center: { lat: 38.5, lng: -76.5 },
    zoom: 8,
  });

console.log("AJAX request started");

/*
AJAX connects to VA json file and extracts data
Uses data to populate map with markers at specific Longitude/Latitude
*/
$.ajax({
    url: 'static/json/Va_Permit.json',
    type:"GET",
    dataType: 'json',
    success: function(data) {
        console.log("AJAX request completed successfully");

        // Use the data to map points on the map
         // Use the data given in json file
      data.forEach(function(point) {
        let mapCode = point.Hydrocode;
        let desc1 = point.Source_Type;
        let latitude = parseFloat(point.Latitude);
        let longitude = parseFloat(point.Longitude);
        let locality = point.Locality;
        let point1 = parseFloat(point.Year_2016);
        let point2 = parseFloat(point.Year_2017);
        let point3 = parseFloat(point.Year_2018);
        let point4 = parseFloat(point.Year_2019);
        let point5 = parseFloat(point.Year_2020);

        // Uses latitude and longitude to map points on the map
        var marker = new google.maps.Marker({
            position: { lat: latitude, lng: longitude },
            map: map,
            title: mapCode,
            descriptions: {
              description1: desc1,
              description2: locality
          },
          points: {
            point1: point1,
            point2: point2,
            point3: point3,
            point4: point4,
            point5: point5
          }
        });
            markers.push(marker);
            const infowindow = new InfoWindow({
              content: `
              <div class = "info-window">
              <strong>${marker.title}</strong>
              </div>
              `,
              maxWidth: 300,
            });

            marker.addListener('mouseover', () => {
              if (!window.popupLayerOpen || marker !== window.currentMarker) {
                infowindow.open(map, marker);
              }
            });
        
            marker.addListener('mouseout', () => {
              if (!window.popupLayerOpen || marker !== window.currentMarker) {
                infowindow.close();
              }
            });
            //adds interactive function to marker on click
            marker.addListener("click", () => {
              popUpLayer1(marker, map);
              infowindow.close();
              window.popupLayerOpen = true;
            });
           
            
        });

        const markerCluster = new MarkerClusterer(map, markers, {
          imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m',
          gridSize: 50, // Adjust as needed
          maxZoom: 15 // Adjust as needed
        });
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});

}

//closes popup upon clicking overlay
document.getElementById('overlay').addEventListener('click', closePopup);

//handles enter key for search()
function handleKeyPress(event) {
  if (event.keyCode === 13) {
    const searchInput = document.getElementById("search-input").value.trim();
    if (searchInput !== "") {
      search(markers, map);
    }
  }
}
//event listener for search enter press
document.getElementById("search-input").addEventListener("keypress", handleKeyPress);
//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
