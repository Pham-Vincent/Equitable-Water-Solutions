/*
title: legend.js

Description: This file holds all the methods for handling legend functionality then exporting to 'script.js'.
Functions handle removing markers and adding back markers using specified usetype 'id'

Authors: W. Lamuth, N. Gammel

Date: 04/25/24
*/

import { markers, map, markerCluster, shown } from './script.js';


//sets all markers in given array to visible or invisible(used for legend)
export function setMapOnAll(map, Tmarkers, id=null) {
    //this removes Virginia points, as id == null and removes clustering on all Virginia
    if(map==null){
        markerCluster.removeMarkers(Tmarkers);
        console.log('markeres removed');
    }
  
    for (let i = 0; i < Tmarkers.length; i++) {
        if(Tmarkers[i].descriptions.visible == shown[1]){
            Tmarkers[i].descriptions.visible = shown[0]
        } else {
            Tmarkers[i].descriptions.visible = shown[1]
        }
        Tmarkers[i].setMap(map);
    }
  
    if(map!=null){
      markerCluster.addMarkers(Tmarkers);
      console.log('markeres added');
    }
  }
  
/*
Name: legendFunc
Usage: Pass in an id that matches with corresponding tag associated with each marker.
        Using this we can use a single function to make a fully functioning legend.
*/
export function legendFunc(id) {

    //finds checkbox id
    const checkbox = document.getElementById(id).querySelector('input[type="checkbox"]');
    console.log(id);

    const tempMarkers = markers.filter(marker => marker.descriptions && marker.descriptions.tag === id);

    //if checked -> show markers
    if (checkbox.checked) {
        setMapOnAll(map, tempMarkers, id);
        console.log("Checkbox is checked");
    } 
    //if unchecked -> hide markers
    else {
        console.log("Checkbox is unchecked");
        setMapOnAll(null, tempMarkers, id);
    }
}

/*
Name: selectAll

Usage: if select all is checked all boxes checked and all markers shown. 
If unchecked it unchecks all checkboxes and removes all markers
*/
export function selectAll(id, source){

    const selectAllBox = document.getElementById(id).querySelector('input[type="checkbox"]');
    console.log(id);

    //finds all checkboxes with name attritbute = box
    const checkboxes = document.getElementsByName("box");
    //parses for MD markers only
    const tempMarkers = markers.filter(marker => marker.descriptions && marker.descriptions.tag != 'Virginia');

    //checks/unchecks all boxes depending on 'Select All' box status 
    for(var i=0;i<checkboxes.length;i++) 
        checkboxes[i].checked = source.checked;

    //if checked -> show markers, else -> hide markers
    if(selectAllBox.checked)
        setMapOnAll(map, tempMarkers);
    else
        setMapOnAll(null, tempMarkers);
}

//makes functions globally accessible
window.legendFunc = legendFunc;
window.setMapOnAll = setMapOnAll;
window.selectAll = selectAll;