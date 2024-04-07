/* 
title: search.js

Authors: William Lamuth

Description: This file contains functions for handling the search bar functionality in the application. 
It exports 'search()', to script.js. The 'search()' function takes an array of markers 
and the map object as input and performs a case-insensitive search for a specified keyword in the titles of markers. 
If a match is found, it zooms and centers the map on the matching marker's position and opens an info window to highlight the marker. 
Otherwise, it logs a message indicating that no match was found.

Date: 04/06/24
*/

export function search(markers, map) {
    const searchInput = document.getElementById("search-input").value.trim().toLowerCase();
  
    markers.forEach(marker => {
      const markerTitle = marker.title.toLowerCase();
  
      //currently zooms and centers on marker. opens infowindow to highlight
      if (markerTitle.includes(searchInput)) {
        console.log("Match found!");
        map.panTo(marker.position);
        map.setZoom(15);
        popUpLayer1(marker, map);
        window.popupLayerOpen = true;
      } else {
        console.log("Not found");
      }
    });
  }

  