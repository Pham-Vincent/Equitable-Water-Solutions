/*
title: markerFunctions.js

Description: This file holds methods for handling marker customization then exports to 'script.js'.
Defines functions that handle marker action listeners and customizing marker graphics

Authors: W. Lamuth, V. Pham, N. Gammel

Date: 04/21/24
*/
import { popUpLayer1, openPopup, closePopup, viewMore } from './popup.js';

//sets marker image depending on designated use
export function setMarkerIcon(designatedUse){
    if (designatedUse === "Mining") {
        return "static/images/pickaxe.png";
    }
    if (designatedUse === "Fire and Hyrdrostatic") {
        return "static/images/flame.png";
    }
    if (designatedUse === "Power Related") {
        return "static/images/square.png";
    }
    if (designatedUse === "Institutional Use") {
        return "static/images/circle.png";
    }
    if (designatedUse === "Industrial Use") {
        return "static/images/diamond.png";
    }
    if (designatedUse === "Commercial Use") {
        return "static/images/pentagon.png";
    }
    if (designatedUse === "Other Irrigation") {
        return "static/images/star-2.png";
    }
    if (designatedUse === "Crop Irrigation") {
        return "static/images/corn.png";
    }
    if (designatedUse === "Drinking") {
        return "static/images/hexagon.png";
    }
    if(designatedUse === "Aquaculture"){
        return "static/images/triangle.png";
    }
}

//Simplified Function to add listeners to every marker
export function addListeners(marker, infowindow, map) {
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
}