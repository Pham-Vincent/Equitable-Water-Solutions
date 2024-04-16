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
let map;
let markers = []; //stores markers used in search()
let markersMD = []; //array used in legend function showVA()
let markersVA = []; //array used in legend function showMD()


function Load_Map(){

  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r,"places","marker"].join(","));for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:"):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}

async function initMap() {
  await Load_Map()
  const { Map, InfoWindow, MarkerClusterer} = await google.maps.importLibrary("maps", "markerclusterer");
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
        let mType = 'm';

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
            content: glyphImg,
        });

        // Attach custom properties to the marker object
        marker.descriptions = {
          description1: desc1,
          description2: locality,
          description3: mType
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
        
        markersVA.push(marker);  
        //creates infowindow used in hover listeners
        const infowindow = new InfoWindow({
          content: `
            <div class = "info-window">
            <strong>${marker.title}</strong>
            </div>
            `,
            maxWidth: 300,
        });

        //Event listener for hovering
        marker.content.addEventListener('mouseenter', ({ domEvent }) => {
          if (!window.popupLayerOpen || marker !== window.currentMarker) {
            infowindow.open(map, marker);
          }
        });
        
        //Event listener for closing hovering
        marker.content.addEventListener('mouseleave', () => {
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

        //if infowindow wont close on 'mouseleave' clicking the map will close

        google.maps.event.addListener(map, 'click', function() {
          // Check if the info window is open
          if (infowindow) {
              // Close the info window
              infowindow.close();
          }
        });


            
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
      let mapCode = point.PermitNumber;
      let desc1 = point.DesignatedUse;
      let latitude = parseFloat(point.FixedLatitudes);
      let longitude = parseFloat(point.FixedLongitudes);
      let locality = point.County;
      let fresh = point.FreshwaterOrSaltwater;
      let tidal = point.TidalorNontidal;


      //uses triangle.png as marker
      const glyphImg = document.createElement("img");
      glyphImg.src = "static/images/hexagon.png"
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
        description4: desc1
      };
      
      //marker pushed into markers array, used in search()
      markers.push(marker); 
      // temp array to store MD points
      markersMD.push(marker); 
          
      //creates infowindow used in hover listeners
      const infowindow = new InfoWindow({
        content: `
          <div class = "info-window">
          <strong>${marker.title}</strong>
          </div>
          `,
          maxWidth: 300,
      });

      //Event listener for hovering
      marker.content.addEventListener('mouseenter', ({ domEvent }) => {
        if (!window.popupLayerOpen || marker !== window.currentMarker) {
          infowindow.open(map, marker);
        }
      });
      
      //Event listener for closing hovering
      marker.content.addEventListener('mouseleave', () => {
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

      //if infowindow wont close on 'mouseleave' clicking the map will close
      google.maps.event.addListener(map, 'click', function() {
        if (infowindow) {
            infowindow.close();
        }
      });
         
          
    });

      
  },
  error: function(xhr, status, error) {
      console.error('Error:', error);
  }
});


$(document).ajaxStop(function() {
  const markerCluster = new markerClusterer.MarkerClusterer({ 
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
function setMapOnAll(map, markers) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

//hides markers for MD(used for legend)
function showMD() {

  //finds checkbox with id = "legend-Mining"
  const checkbox = document.getElementById("legend-Mining").querySelector('input[type="checkbox"]');
    
    //if checked -> show markers
    if (checkbox.checked) {
      setMapOnAll(map, markersMD);
      console.log("Checkbox is checked");
    } 
    //if unchecked -> hide markers
    else {
      console.log("Checkbox is unchecked");
      setMapOnAll(null, markersMD);
    }
}

//hides markers for VA(used for legend)
function showVA() {

  //finds checkbox with id = "legend-Withdrawal"
  const checkbox = document.getElementById("legend-Withdrawal").querySelector('input[type="checkbox"]');
    
    //if checked -> show markers
    if (checkbox.checked) {
      setMapOnAll(map, markersVA);
      console.log("Checkbox is checked");
    } 
    //if unchecked -> hide markers
    else {
      console.log("Checkbox is unchecked");
      setMapOnAll(null, markersVA);
    }
}

window.showMD = showMD;
window.showVA = showVA;
window.setMapOnAll = setMapOnAll;

//event listener for search enter press
document.getElementById("search-input").addEventListener("keypress", handleKeyPress);
//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
