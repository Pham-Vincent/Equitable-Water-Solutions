/*
title: markerFunctions.js

Description: This file holds methods for handling marker customization then exports to 'script.js'.
Defines functions that handle marker action listeners and customizing marker graphics

Authors: W. Lamuth, V. Pham, N. Gammel

Date: 04/21/24
*/
import { openInfoWindow2 } from './popup.js';
import { addCircle, markerCircle, removeCircle } from './marker-radius.js';

//sets marker glyph depending on designated use
export function setMarkerIcon(designatedUse){
    if (designatedUse === "Mining") {
        return "static/images/pickaxe.png";
    }
    if (designatedUse === "Fossil Power") {
        return "static/images/flame.png";
    }
    if (designatedUse === "Municipal") {
        return "static/images/institution.png";
    }
    if (designatedUse === "Manufacturing") {
        return "static/images/nuclearicon.png";
    }
    if (designatedUse === "Industrial") {
        return "static/images/factory.png";
    }
    if (designatedUse === "Commercial") {
        return "static/images/dollar.png";
    }
    if (designatedUse === "Irrigation") {
        return "static/images/irrigation.png";
    }
    if (designatedUse === "Agriculture") {
        return "static/images/wheat.png";
    }
    if (designatedUse === "Other") {
        return "static/images/water-bottle.png";
    }
    if(designatedUse === "Aquaculture"){
        return "static/images/waterdroplet.png";
    }
    if(designatedUse === "Nuclear Power"){
      return "static/images/power.png";
  }
    
}

//Simplified Function to add listeners to every marker
export function addListeners(marker, infowindow, map, infowindow2, glyphElement) {
  //Event listener for opening infowindow on hoverover
  marker.content.addEventListener('mouseenter', () => {
    if (!window.isInfoWindow2Open || marker !== window.currentMarker) {
      infowindow.open(map, marker);
      addCircle(map, marker);
    }
    //changes marker color on hoverover
    if(marker.descriptions.state != 'Virginia')
      glyphElement.background = '#ffd966';
    if(marker.descriptions.state != 'Maryland')
      glyphElement.background = '#ea9999';
  });
  
  //Event listener for closing infowindow on hoverout
  marker.content.addEventListener('mouseleave', () => {
    if (!window.isInfoWindow2Open || marker !== window.currentMarker) {
      infowindow.close();
      removeCircle(map, marker);
    }
    //reverts marker color on hoverout
    if(marker.descriptions.state != 'Virginia')
      glyphElement.background = '#fe9f3b';
    if(marker.descriptions.state != 'Maryland')
      glyphElement.background = '#e06666';
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

//Helper function to create the content for the cluster marker
export function createClusterContent(count) {
  const div = document.createElement('div');
  div.style.position = 'relative';
  div.style.width = '50px';
  div.style.height = '50px';
  div.style.display = 'flex';
  div.style.alignItems = 'center';
  div.style.justifyContent = 'center';

  //Add the icon image
  const img = document.createElement('img');
  img.src = 'static/images/clustericondarkblue.png'; //src determines the icon image
  img.style.width = '60px';
  img.style.height = '60px';
  div.appendChild(img);

  //Add the marker count
  const label = document.createElement('span');
  label.innerText = String(count);
  label.style.color = 'white';
  label.style.fontSize = '14px';
  label.style.position = 'absolute';
  div.appendChild(label);

  return div;
}

