/* 
title: MarkerPinning.js

Authors: Vincent Pham

Description: This file contains methods for handling marker Pinning and exporting them into a Database for the dashboard later

Date: 9/7/24
*/


export function pinLocation(title){
  
  
  fetch('/session-data')
  .then(response => response.json())
  .then(data => {
    if(data.id == null){
      alert('Need To Login')
    }else{
      fetch('/pin-location',
      {
        method:'POST',
        headers:{
          'Content-Type': 'application/json'
        },
        body:JSON.stringify({hydrocode:title, userid:data.id})
      })
      
    }
})}


window.pinLocation = pinLocation;