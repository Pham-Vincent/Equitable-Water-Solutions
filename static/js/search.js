/* 
title: search.js
Description: Handles search bar functionality
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

  