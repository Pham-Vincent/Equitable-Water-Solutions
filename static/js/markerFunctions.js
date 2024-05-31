/*
title: markerFunctions.js

Description: This file holds methods for handling marker customization then exports to 'script.js'.
Defines functions that handle marker action listeners and customizing marker graphics

Authors: W. Lamuth, V. Pham, N. Gammel

Date: 04/21/24
*/
import { openInfoWindow2 } from './popup.js';

//sets marker glyph depending on designated use
export function setMarkerIcon(designatedUse){
    if (designatedUse === "Mining") {
        return "static/images/pickaxe.png";
    }
    if (designatedUse === "Fire and Hyrdrostatic") {
        return "static/images/flame.png";
    }
    if (designatedUse === "Power Related") {
        return "static/images/power.png";
    }
    if (designatedUse === "Institutional Use") {
        return "static/images/institution.png";
    }
    if (designatedUse === "Industrial Use") {
        return "static/images/factory.png";
    }
    if (designatedUse === "Commercial Use") {
        return "static/images/dollar.png";
    }
    if (designatedUse === "Other Irrigation") {
        return "static/images/irrigation.png";
    }
    if (designatedUse === "Crop Irrigation") {
        return "static/images/wheat.png";
    }
    if (designatedUse === "Drinking") {
        return "static/images/water-bottle.png";
    }
    if(designatedUse === "Aquaculture"){
        return "static/images/waterdroplet.png";
    }
}

//Simplified Function to add listeners to every marker
export function addListeners(marker, infowindow, map, infowindow2, glyphElement) {
  //Event listener for opening infowindow on hoverover
  marker.content.addEventListener('mouseenter', () => {
    if (!window.isInfoWindow2Open || marker !== window.currentMarker) {
      infowindow.open(map, marker);
    }

    //changes MD marker color upon hover
    if(marker.descriptions.tag != 'Virginia'){
      glyphElement.background = '#6fa8dc';
    }
  
  });
  
  //Event listener for closing infowindow on hoverout
  marker.content.addEventListener('mouseleave', () => {
    if (!window.isInfoWindow2Open || marker !== window.currentMarker) {
      infowindow.close();
    }

    //changes MD marker color upon hover
    if(marker.descriptions.tag != 'Virginia'){
      glyphElement.background = 'orange';
    }
  });
      
  //opens/closes infowindow2 with click
  marker.addListener("click", () => {
    if(window.isInfoWindow2Open && marker === window.currentMarker){
      infowindow2.close();
      window.isInfoWindow2Open = false;
    }
    else{
      openInfoWindow2(marker, map, infowindow2);
      infowindow.close();
    }
  });
  
  //if infowindow wont close on 'mouseleave', clicking the map will close infowindow
  google.maps.event.addListener(map, 'click', function() {
    if (infowindow) {
        infowindow.close();
    }
  });

  //clicking on the chesapeake overlay closes infowindow
  map.data.addListener('click', function(event) {
    infowindow2.close();
    window.isInfoWindow2Open = false;
  });  

}