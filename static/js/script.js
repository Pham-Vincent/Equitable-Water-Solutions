/*
Title: script.js
Author: Nicholas Gammel, William Lamuth, Vincent Pham

Functionality: This javascript file will load the Google Maps API, create a map centered on Chesapeake Bay, 
fetch data from a JSON file, create Advanced Markers for each data point, and add event listeners for mouseover, 
mouseout, and click events on each marker. Additionally, it handles search functionality and closing popups.

Output: JavaScript file


Date: 04/16/24

*/
//Gets Google Maps APi Key
import config from './config.js';
import { popUpLayer1, openPopup, closePopup, viewMore } from './popup.js';
import { search } from './search.js';
import { setMarkerIcon, addListeners} from './markerFunctions.js';

let map;
let markers = []; //stores markers used in search()


function Load_Map(){

  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r,"places","marker"].join(","));for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}

async function initMap() {
  await Load_Map()
  const { Map, InfoWindow, Markerclusterer} = await google.maps.importLibrary("maps", "markerclusterer");
  const { AdvancedMarkerElement, PinElement} = await google.maps.importLibrary("marker");
  //creates map instance, map centered on chesapeake bay
  map = new Map(document.getElementById("map"), {
    center: { lat: 38.5, lng: -76.5 },
    zoom: 8,
    
    mapId: "DEMO_MAP_ID",
    scrollwheel:true, //bypasses command+scroll to zoom
  });

  /* Sets the Maximum Zoom out Value */
  map.setOptions({ minZoom: 3});

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
        let mapCode = point.Hydrocode,
        desc1 = point.Source_Type,
        latitude = parseFloat(point.Latitude),
        longitude = parseFloat(point.Longitude),
        locality = point.Locality,
        point1 = parseFloat(point.Year_2016), point2 = parseFloat(point.Year_2017), point3 = parseFloat(point.Year_2018), point4 = parseFloat(point.Year_2019), point5 = parseFloat(point.Year_2020),
        legendType = 'Virginia';

        //custom colored marker
        const pinBackground = new PinElement({
          background: '#0443fb',
          borderColor: '#000000',
          glyphColor: 'white',
        });
        
        //uses triangle.png as marker
        const glyphImg = document.createElement("img");
        glyphImg.src = "static/images/triangle.png"

        //marker with image icon
        const glyphElement = new PinElement({
          background: '#0443fb',
          borderColor: '#000000',
          glyph: glyphImg,
        });

        // Uses latitude and longitude to map points on the map
        var marker = new AdvancedMarkerElement({
            position: { lat: latitude, lng: longitude },
            map,
            title: mapCode,
            //content: glyphImg, // revert marker to default
        });

        // Attach custom properties to the marker object
        marker.descriptions = {
          description1: desc1,
          description2: locality,
          tag: legendType
        };

        marker.points = {
          point1: point1,
          point2: point2,
          point3: point3,
          point4: point4,
          point5: point5,
        };
        
        //marker pushed into markers array, used in search()
        markers.push(marker); 
        
        //creates infowindow used in hover listeners
        const infowindow = new InfoWindow({
          content: `
            <div class = "info-window">
            <strong>${marker.title}</strong>
            </div>
            `,
            maxWidth: 300,
        });

        addListeners(marker, infowindow, map);
            
      });
    
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});


/*
AJAX connects to MD json file and extracts data
Uses data to populate map with markers at specific Longitude/Latitude
*/
$.ajax({
  url: 'static/json/MD_Tidal.json',
  type:"GET",
  dataType: 'json',
  success: function(data) {
      console.log("AJAX request completed successfully");

      // Use the data to map points on the map
       // Use the data given in json file
    data.forEach(function(point) {
      let mapCode = point.PermitNumber,
      desc1 = point.DesignatedUse,
      latitude = parseFloat(point.FixedLatitudes),
      longitude = parseFloat(point.FixedLongitudes),
      locality = point.County,
      fresh = point.FreshwaterOrSaltwater,
      tidal = point.TidalorNontidal;


      //uses triangle.png as marker default
      const glyphImg = document.createElement("img");

      // Uses latitude and longitude to map points on the map
      var marker = new AdvancedMarkerElement({
          position: { lat: latitude, lng: longitude },
          map,
          title: mapCode,
          content: glyphImg,
      });

      // Attach custom properties to the marker object
      marker.descriptions = {
        description1: locality,
        description2: fresh,
        description3: tidal,
        tag: desc1
      };

      console.log(marker.descriptions.tag);
      //sets unique marker icon depending on designated use type
      marker.content.src = setMarkerIcon(marker.descriptions.tag);
          
      //marker pushed into markers array, used in search()
      markers.push(marker); 
          
      //creates infowindow used in hover listeners
      const infowindow = new InfoWindow({
        content: `
          <div class = "info-window">
          <strong>${marker.title}</strong>
          </div>
          `,
          maxWidth: 300,
      });
         
      addListeners(marker, infowindow, map);
          
    });

      
  },
  error: function(xhr, status, error) {
      console.error('Error:', error);
  }
});


$(document).ajaxStop(function() {
  markerClusterer = new markerClusterer.MarkerClusterer({ 
    map,
    markers:markers,
    algorithmOptions:{radius:150}
  });

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

//sets all markers in given array to visible or invisible(used for legend)
function setMapOnAll(map, Tmarkers, id=null) {
  //this removes Virginia points, as id == null and removes clustering on all Virginia
    if(map==null){
      markerClusterer.removeMarkers(Tmarkers);
    }

  for (let i = 0; i < Tmarkers.length; i++) {
    Tmarkers[i].setMap(map);
  }

  if(map!=null){
    markerClusterer.addMarkers(Tmarkers);
  }
}

/*
Name: legendFunc
Usage: Pass in an id that matches with corresponding tag associated with each marker.
       Using this we can use a single function to make a fully functioning legend.
*/
function legendFunc(id) {

  //finds checkbox with id = "legend-Mining"
  const checkbox = document.getElementById(id).querySelector('input[type="checkbox"]');
  console.log(id);

  const tempMarkers = markers.filter(marker => marker.descriptions && marker.descriptions.tag === id);
    //if checked -> show markers
    if (checkbox.checked) {
      setMapOnAll(map, tempMarkers, id);
      console.log("Checkbox is checked");
    } 
    //if unchecked -> hide markers
    else {
      console.log("Checkbox is unchecked");
      setMapOnAll(null, tempMarkers, id);
    }
}

window.legendFunc = legendFunc;
window.setMapOnAll = setMapOnAll;

//event listener for search enter press
document.getElementById("search-input").addEventListener("keypress", handleKeyPress);
//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
