/* 
title: popup.js

Authors: William Lamuth, Vincent Pham, Nicholas Gammel

Description: This file contains methods for handling marker popups and exports them to script.js. 
It defines functions for displaying various layers of information associated with markers on a Google Map, 
including a basic popup, a detailed popup with additional content and a graph, and a view more button to toggle between popups. 
The functions allow users to interact with markers on the map by displaying relevant information and additional details when clicked.

Date: 04/06/24
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
  
    //creates first layer infowindow
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

//Function to open the full popup
export function openPopup(marker, currentGraph) {
    customPopup = document.getElementById('popup');
    customPopup.innerHTML = `
      <h1>${marker.title}</h1>
      <div class="info-window">
        <p>${marker.descriptions.description1}</p>
        <p>${marker.descriptions.description2}</p>
  
        <img id ="Graph">
        <button id ="btn">Click to Graph</button>
  
        <div id="close-button" onclick="closePopup()">X</div>
      </div>
    `;
    customPopup.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    
    $("#btn").click(preformPost);
  
    //Function to handle button click event for generating the graph
    function preformPost(){
      $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_graph",
        data: marker.points,
        success: function(response){
          $('#Graph').attr('src', response.src);
          $('#Graph').attr('alt', response.alt);
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





