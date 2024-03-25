//Gets Google Maps APi Key
import config from './config.js';
let map;
let customPopup;
let markersData;
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
              if (!window.popupLayerOpen && marker.getTitle(0 != window.popupTitle)) {
                infowindow.open(map, marker);
              }
            });
        
            marker.addListener('mouseout', () => {
              if (!window.popupLayerOpen) {
                infowindow.close();
              }
            });
            //adds interactive function to marker on click
            marker.addListener("click", () => {
              popUpLayer1(marker);
              infowindow.close();
              window.popupLayerOpen = true;
            });
           
            
        });
    },
    error: function(xhr, status, error) {
        console.error('Error:', error);
    }
});

}


//first layer popup
function popUpLayer1(marker){
  //Close the currently open info window, if any
  if (window.smallInfowindow) {
    window.smallInfowindow.close();
  }
  
  const popupTitle = marker.getTitle();

  const smallInfowindow = new google.maps.InfoWindow({
    content: `
      <div class="info-window">
        <strong>${marker.getTitle()}</strong>

        <p>${marker.descriptions.description1}</p>
        <p>${marker.descriptions.description2}</p>

        <button id="view-more-button" onclick="viewMore('${marker.graph}')">View More</button>

      </div>
    `,
    maxWidth: 300,
  });
  //closes window if clicking outside
  google.maps.event.addListener(map, 'click', function () {
    smallInfowindow.close();
    window.popupLayerOpen = false;
  });
  
  smallInfowindow.open(map, marker);
  window.currentMarker = marker;
  window.smallInfowindow = smallInfowindow;
  window.popupTitle = popupTitle;

  smallInfowindow.addListener('closeclick', () => {
    window.popupLayerOpen = false;
  });

  
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
      <p>${marker.descriptions.description1}</p>
      <p>${marker.descriptions.description2}</p>

      // Id that will be replaced by image
      <img id ="Graph">
      <button id ="btn">Click to Graph</button>

      <div id="close-button" onclick="closePopup()">X</div>
    </div>
  `;
  customPopup.style.display = 'block';
  document.getElementById('overlay').style.display = 'block';
  
  $("#btn").click(preformPost);

  // Function to handle button click event for generating the graph
  function preformPost(){
   $.ajax({ 
    type:"POST",
    url:"http://127.0.0.1:5000/create_graph",
    data: marker.points,
     success: function(response){
      $('#Graph').attr('src', response.src);
      $('#Graph').attr('alt', response.alt);
    }
  });
  
};

  
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

//Calls function to load the map 
Load_Map();
//Calls function to details to the map (Markers,Legend,etc)
initMap();
