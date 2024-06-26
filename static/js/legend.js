/*
title: legend.js

Description: This file holds all the methods for handling legend functionality then exporting to 'script.js'.
Functions handle removing markers and adding back markers using specified usetype 'id'

Authors: W. Lamuth, N. Gammel

Date: 04/25/24
*/

import { markers, map, markerCluster, shown } from './script.js';
let checkboxes;

//Creates Hashmap data structure - default value is true as they are shown by default
//useTypes is general term, likely to be changed
var states = ['Maryland', 'Virginia'];
var tags = ['Agriculture', 'Aquaculture','Commercial','Fossil Power', 'Industrial','Irrigation','Manufacturing','Mining','Municipal','Nuclear Power','Other'];

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

/*
Name: setMapOnAll

Usage: Pass in map, a list of markers, and the id of attribute to adjust the markers being shown/hidden on the map.
*/
//sets all markers in given array to visible or invisible(used for legend)
export function setMapOnAll(map, Tmarkers, id=null) {
    //map is null when you toggle to remove markers
    if(map==null){
        //Switch from visible id to non-visible id
        useTypes.set(id,false);
        markerCluster.removeMarkers(Tmarkers);
        //Hides hidden markers for search
        Tmarkers.forEach(marker => marker.descriptions.visible = shown[0]);
        return;
    }
    //Since map is not null in this case, we are adding markers to the map
    //So we set the input id to true
    useTypes.set(id,true);

    //creates two new sub-arrays to store values for batch system
    const markersToAdd = [];
  
    for (let i = 0; i < Tmarkers.length; i++) {
        const stateVisible = useTypes.get(Tmarkers[i].descriptions.state);
        const tagVisible = useTypes.get(Tmarkers[i].descriptions.tag);

        //If the state and tag are visible, then the markers within Tmarkers are shown on the map
        if(stateVisible && tagVisible){
            markersToAdd.push(Tmarkers[i]);
            Tmarkers[i].setMap(map);
            //Shows revealed markers for search
            Tmarkers[i].descriptions.visible = shown[1]
        }
    }

    //Batch System Updates to add all markers in one push, improving performance
    if(markersToAdd.length > 0){
        markerCluster.addMarkers(markersToAdd);
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

    //Chooses which boxes to select/unselect depending on id Use Types or States
    if(id==='Select All States'){
         checkboxes = document.getElementsByName("states");
    }
    else{
         checkboxes = document.getElementsByName("type");
    }
    
    //checks/unchecks all boxes depending on 'Select All' box status 
    for(var i=0;i<checkboxes.length;i++) 
        checkboxes[i].checked = source.checked;

    //if checked -> show markers, else -> hide markers
    if(selectAllBox.checked){
        setAllMapValues(map,id);
        setMapOnAll(map, markers);
    }
    else {
        setAllMapValues(null,id);
        setMapOnAll(null, markers);
    }
}

/*
Name: setAllMapValuesToFalse

Usage:If selectAll function is called, this will be a simple way to adjust all attributes
*/
function setAllMapValues(map,id) {
    //loops through states
    if(id==='Select All States'){
        states.forEach(state => useTypes.set(state, map==null?false:true));
    }
    //loops through all tags
    else{
        tags.forEach(tag => useTypes.set(tag, map==null?false:true));
    }
}
//makes functions globally accessible
window.legendFunc = legendFunc;
window.setMapOnAll = setMapOnAll;
window.selectAll = selectAll;