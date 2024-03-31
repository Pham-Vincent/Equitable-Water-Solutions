//searchFunctions.js

export function search(markers, map) {
    const searchInput = document.getElementById("search-input").value.trim().toLowerCase();
  
    markers.forEach(marker => {
      const markerTitle = marker.getTitle().toLowerCase();
  
      if (markerTitle.includes(searchInput)) {
        console.log("Match found!");
        map.panTo(marker.getPosition());
        map.setZoom(15);
        popUpLayer1(marker, map);
        window.popupLayerOpen = true;
      } else {
        console.log("Not found");
      }
    });
  }

  