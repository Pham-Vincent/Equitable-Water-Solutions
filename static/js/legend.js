/*
title: legend.js

Description: This file holds all the methods for handling legend functionality then exporting to 'script.js'.
Functions handle removing markers and adding back markers using specified usetype 'id'

Authors: W. Lamuth, N. Gammel

Date: 04/25/24
*/

import { markers, map, markerCluster, shown } from './script.js';
let tempMarkers;

//Creates Hashmap-like data structure
//NAME SUBJECT TO CHANGE
var useTypes = new Map;
useTypes.set('Maryland',true);
useTypes.set('Virginia',true);
useTypes.set('Agriculture',true);
useTypes.set('Aquaculture',true);
useTypes.set('Commercial',true);
useTypes.set('Fossil Power',true);
useTypes.set('Industrial',true);
useTypes.set('Irrigation',true);
useTypes.set('Manufacturing',true);
useTypes.set('Mining',true);
useTypes.set('Municipal',true);
useTypes.set('Nuclear Power',true);
useTypes.set('Other',true);


//sets all markers in given array to visible or invisible(used for legend)
export function setMapOnAll(map, Tmarkers, id=null) {
    //Switch from visible id to non-visible id
    //this removes Virginia points, as id == null and removes clustering on all Virginia
    if(!useTypes.has(id)){
        useTypes.set(id,true);
    }

    if(map==null){
        //Switch from visible id to non-visible id
        useTypes.set(id,false);
        markerCluster.removeMarkers(Tmarkers);
    }
    else{
        useTypes.set(id,true);
    }
  
    for (let i = 0; i < Tmarkers.length; i++) {
        //Related to only SEARCHING for shown markers
        if(Tmarkers[i].descriptions.visible == shown[1]){
            Tmarkers[i].descriptions.visible = shown[0]
        } else {
            Tmarkers[i].descriptions.visible = shown[1]
        }
        //Checks if State ID is Shown and Usetype ID is shown
        //Account for map == null && state == false && tag == false
        console.log(Tmarkers[i].descriptions.state);
        console.log(useTypes.get(Tmarkers[i].descriptions.state));
        console.log(useTypes.get(Tmarkers[i].descriptions.tag));
        if(map != null && useTypes.get(Tmarkers[i].descriptions.state) == true && useTypes.get(Tmarkers[i].descriptions.tag) == true){
            Tmarkers[i].setMap(map);
            markerCluster.addMarker(Tmarkers[i]);
        }
        else{
            Tmarkers[i].setMap(null);
        }  
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
    let tempMarkers;
    if(id === "Maryland"||id === "Virginia"){
        tempMarkers = markers.filter(marker => marker.descriptions && marker.descriptions.state === id);
    }
    else{
        tempMarkers = markers.filter(marker => marker.descriptions && marker.descriptions.tag === id);
    }
    //if checked -> show markers
    if (checkbox.checked) {
        setMapOnAll(map, tempMarkers, id);
    } 
    //if unchecked -> hide markers
    else {
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

    //finds checkboxes elements with name="box" in index.html
    const checkboxes = document.getElementsByName("box");
    
    //checks/unchecks all boxes depending on 'Select All' box status 
    for(var i=0;i<checkboxes.length;i++) 
        checkboxes[i].checked = source.checked;

    //if checked -> show markers, else -> hide markers
    if(selectAllBox.checked)
        setMapOnAll(map, markers);
    else
        setMapOnAll(null, markers);
}

//makes functions globally accessible
window.legendFunc = legendFunc;
window.setMapOnAll = setMapOnAll;
window.selectAll = selectAll;