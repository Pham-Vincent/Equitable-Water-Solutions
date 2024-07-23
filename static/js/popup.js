/* 
title: popup.js

Authors: William Lamuth, Vincent Pham, Nicholas Gammel

Description: This file contains methods for handling marker popups and exports them to script.js. 
It defines functions for displaying various layers of information associated with markers on a Google Map, 
including a basic popup, a detailed popup with additional content and a graph, and a view more button to toggle between popups. 
The functions allow users to interact with markers on the map by displaying relevant information and additional details when clicked.

Date: 05/12/24
*/
import config from './config.js';
let customPopup;

//first layer popup
export function openInfoWindow2(marker, map, infowindow2){
    
    window.isInfoWindow2Open = true;

    //Close the currently open info window, if any
    if (window.infowindow2) {
      window.infowindow2.close();
    }  

    //closes window if clicking outside
    google.maps.event.addListener(map, 'click', function () {
      infowindow2.close();
      window.isInfoWindow2Open = false;
    });

    infowindow2.open(map, marker); 
    
    window.currentMarker = marker;
    window.infowindow2 = infowindow2;
  
    //when clicking 'X' to close infowindow, sets isInfoWindow2Open to false
    infowindow2.addListener('closeclick', () => {
      window.isInfoWindow2Open = false;
    });
  
}

//Function to open the full information display window
export function openPopup(marker) {
  
    //finds html id 'popup' and defines inner content
    customPopup = document.getElementById('popup');
    customPopup.innerHTML = `
        <h1 class="popup-title">Hydrocode:  <span style="color: #ffe657;">${marker.title}</span></h1>
        <div id="close-button" onclick="closePopup()"><img src="static/images/close-button.png" alt="Close"></div>
        <div class="popup-content">
          <div class="header-paragraph">
            <h3 class="popup-description">Water Source Type:</h3>
            <p>${marker.descriptions.description2}</p>
          </div>
          <div class="header-paragraph">
            <h3 class="popup-description">Area:</h3>
            <p>${marker.descriptions.description1}</p>
          </div>
        
          <div id="graph_html"></div>
          <div id="DepthHeatMap_html"></div>
        </div>   
    `;
    preformPost(marker);
    customPopup.style.display = 'block';
    document.getElementById('overlay').style.display = 'block'; 
  
    //Function to handle button click event for generating the graph
    function preformPost(marker){
      //Only will create Graphs for Virginia
    
    if(marker.descriptions.state == 'Virginia')
      {
        $('#graph_html').addClass("loader")        
      $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_VA_graph",
        data: marker.points,
       success: function(response){
        /*Stops the Loading Screen*/
        $('#graph_html').removeClass("loader")
        $('#graph_html').html(response.graph_json)
       } 
      });
    }
    /*Maryland Tidal Data */
    else
    { 
        $('#graph_html').addClass("loader")
        $('#DepthHeatMap_html').addClass("loader")
        $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_MD_graph",
        data: marker.title, 
       success: function(response){
        /*Stops the Loading Screen*/
        $('#graph_html').removeClass("loader")
        $('#graph_html').html(response.graph_json)
       },
      error:function(error){
      $('#graph_html').removeClass("loader")
       } 
      });
        $.ajax({ 
        type:"POST",
        url:config.hostname + "/create_MultiDepth_graph",
        data: marker.title, 
       success: function(response){
        /*Stops the Loading Screen*/
        $('#DepthHeatMap_html').removeClass("loader")
        $('#DepthHeatMap_html').html(response.Depth_json)
       },
      error:function(error){
      $('#DepthHeatMap_html').removeClass("loader")
       } 
      });
      }
    
    };
}

export function closePopup() {
    customPopup = document.getElementById('popup');
    customPopup.style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
    window.isInfoWindow2Open=false;
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
window.openInfoWindow2 = openInfoWindow2;





