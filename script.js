//Gets Google Maps APi Key
import config from './config.js';
let map;
let customPopup;
let markersData;
function Load_Map(){
  (g=>{var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams,u=()=>h||(h=new Promise(async(f,n)=>{await (a=m.createElement("script"));e.set("libraries",[...r]+"");for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);e.set("callback",c+".maps."+q);a.src=`https://maps.${c}apis.com/maps/api/js?`+e;d[q]=f;a.onerror=()=>h=n(Error(p+" could not load."));a.nonce=m.querySelector("script[nonce]")?.nonce||"";m.head.append(a)}));d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n))})
  ({key:config.apiKey, v: "weekly"});
}

//Calls function to load the map 
Load_Map();


async function initMap() {
  const { Map, Marker, InfoWindow } = await google.maps.importLibrary("maps");

  //creates map instance, map centered on chesapeake bay
  map = new Map(document.getElementById("map"), {
    center: { lat: 38.5, lng: -76.5 },
    zoom: 8,
  });

console.log("AJAX request started");

$.ajax({
    url: 'data.json',
    dataType: 'json',
    success: function(data) {
        console.log("AJAX request completed successfully");

        // Use the data to map points on the map
        data.forEach(function(point) {
            var mapCode = point.ic_site_id;
            var desc1 = point.site_description1;
            var latitude = parseFloat(point.lat_dd);
            var longitude = parseFloat(point.long_dd);

            // Uses latitude and longitude to map points on the map
            var marker = new google.maps.Marker({
                position: { lat: latitude, lng: longitude },
                map: map,
                title: mapCode,
                description: desc1
            });

            const infowindow = new InfoWindow({
              content: `
              <div class = "info-window">
              <strong>${marker.title}</strong>
              </div>
              `,
              maxWidth: 300,
            });

            marker.addListener('mouseover', function() {
              infowindow.open(map,marker);
            });  
            marker.addListener('mouseout', () => {
              infowindow.close();
            });
            //adds interactive function to marker on click
            marker.addListener("click", () => {
              openPopup(marker);
            });
        });
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});


}

//function finds id="popup" then sets HTML content inside the element with id="popup"
function openPopup(marker) {
  customPopup = document.getElementById('popup');
  customPopup.innerHTML = `
    <h1>${marker.getTitle()}</h1>
    <div class="info-window">
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

//makes functions globally available
window.openPopup = openPopup;
window.closePopup = closePopup;



//Calls function to details to the map (Markers,Legend,etc)
initMap();
