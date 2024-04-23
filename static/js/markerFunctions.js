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
        return "static/images/triangle.png";
    }
    if (designatedUse === "Fire and Hyrdrostatic") {
        return "static/images/hexagon.png";
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
        return "static/images/star.png";
    }
}


export function handleHoverOver(map, marker, infowindow){
    marker.content.addEventListener('mouseenter', () => {
        if (!window.popupLayerOpen || marker !== window.currentMarker || !infowindow) {
          infowindow.open(map, marker);
        }
      });
}

export function handleHoverOut(map, marker, infowindow){
    marker.content.addEventListener('mouseleave', () => {
        if (!window.popupLayerOpen || marker !== window.currentMarker) {  
          infowindow.close();
        }
      });
}

export function handleMarkerClick(map, marker, infowindow){
    marker.addListener("click", () => {
        popUpLayer1(marker, map);
        infowindow.close();
        window.popupLayerOpen = true;
      });
}

export function handleInfowindowClick(map, infowindow){
    google.maps.event.addListener(map, 'click', function() {
        if (infowindow) {
            infowindow.close();
        }
      });
}

