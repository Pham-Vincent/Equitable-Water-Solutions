/* 
title: popup.js

Authors: William Lamuth, Vincent Pham, Nicholas Gammel

Description: This file contains methods for handling marker popups and exports them to script.js. 
It defines functions for displaying various layers of information associated with markers on a Google Map, 
including a basic popup, a detailed popup with additional content and a graph, and a view more button to toggle between popups. 
The functions allow users to interact with markers on the map by displaying relevant information and additional details when clicked.

Date: 05/05/24
*/
import config from './config.js';
let customPopup;

//first layer popup
export function popUpLayer1(marker, map, infowindow2){
    //Close the currently open info window, if any

    window.popupLayerOpen = true;

    if (window.infowindow2) {
      window.infowindow2.close();
    }
    
    const popupTitle = marker.title;    

    //closes window if clicking outside
    google.maps.event.addListener(map, 'click', function () {
      infowindow2.close();
      window.popupLayerOpen = false;
    });

    infowindow2.open(map, marker); 
    
    window.currentMarker = marker;
    window.infowindow2 = infowindow2;
    window.popupTitle = popupTitle;
  
    infowindow2.addListener('closeclick', () => {
      window.popupLayerOpen = false;
    });
  
}

//Function to open the full popup
export function openPopup(marker) {
  
    customPopup = document.getElementById('popup');
    customPopup.innerHTML = `
      <div class="popup-window">
        <h1 class="popup-title">Hydrocode: ${marker.title}</h1>

        <div class="header-paragraph">
          <h3 class="popup-description">Water Source Type:</h3>
          <p>${marker.descriptions.description1}</p>
        </div>
        <div class="header-paragraph">
          <h3 class="popup-description">Area:</h3>
          <p>${marker.descriptions.description2}</p>
        </div>
        
        <div id="graph_html"></div>
  
        <div id="close-button" onclick="closePopup()"><img src="static/images/close-button.png" alt="Close"></div>
      </div>
    `;
    preformPost(marker);
    customPopup.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    
    
  
    //Function to handle button click event for generating the graph
    function preformPost(marker){
      //Only will create Graphs for Virginia
    
    if(marker.descriptions.tag == 'Virginia')
      {
        $('#graph_html').addClass("loader")
      $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_MD_graph",
        data: marker.points,
       success: function(response){
        /*Stops the Loading Screen*/
        $('#graph_html').removeClass("loader")
        $('#graph_html').html(response.graph_json)
       } 
      });
    }
    /*Calvert Hills Hard Code*/ 
    else if(marker.title =='CA1971S001(04)')
      { 
        $('#graph_html').addClass("loader")
      $.ajax({ 
        type:"POST",
        url:config.hostname + "/HardCode",
        data: marker.points,
       success: function(response){
        /*Stops the Loading Screen*/
        $('#graph_html').removeClass("loader")
        $('#graph_html').html(response.graph_json)
       } 
      });
      }
    
    };
}


export function closePopup() {
    customPopup = document.getElementById('popup');
    customPopup.style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    window.popupLayerOpen=false;
}

//Function to handle the view more button
export function viewMore() {
    window.infowindow2.close();
    openPopup(window.currentMarker);
}

//Makes functions globally available
window.openPopup = openPopup;
window.closePopup = closePopup;
window.viewMore = viewMore;
window.popUpLayer1 = popUpLayer1;





