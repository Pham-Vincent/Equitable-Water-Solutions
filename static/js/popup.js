/* 
title: popup.js
Description: Contains all methods for handling marker popups
*/
import config from './config.js';
let customPopup;

//first layer popup
export function popUpLayer1(marker, map){
    //Close the currently open info window, if any
    if (window.smallInfowindow) {
      window.smallInfowindow.close();
    }
    
    const popupTitle = marker.title;
  
    const smallInfowindow = new google.maps.InfoWindow({
      content: `
        <div class="info-window">
          <strong style="color:green">${marker.title}</strong>
  
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

//Function to open the popup
export function openPopup(marker, currentGraph) {
    customPopup = document.getElementById('popup');
    customPopup.innerHTML = `
      <h1>${marker.title}</h1>
      <div class="info-window">
        <p>${marker.descriptions.description1}</p>
        <p>${marker.descriptions.description2}</p>
       
        <div id="graph_html"></div>
        ${preformPost()}
  
        <div id="close-button" onclick="closePopup()">X</div>
      </div>
    `;
    customPopup.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    
    
  
    //Function to handle button click event for generating the graph
    function preformPost(){
      $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_graph",
        data: marker.points,
       success: function(response){
        $('#graph_html').html(response.graph_json)

        } 
      });
    };
}


export function closePopup() {
    customPopup = document.getElementById('popup');
    customPopup.style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

//Function to handle the view more button
export function viewMore(currentGraph) {
    window.smallInfowindow.close();
    openPopup(window.currentMarker, currentGraph);
}

//Makes functions globally available
window.openPopup = openPopup;
window.closePopup = closePopup;
window.viewMore = viewMore;
window.popUpLayer1 = popUpLayer1;





