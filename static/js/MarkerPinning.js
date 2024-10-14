/* 
title: MarkerPinning.js

Authors: Vincent Pham

Description: This file contains methods for handling marker Pinning and exporting them into a Database for the dashboard later

Date: 9/7/24
*/


export function checkpinLocation(title,number){
  
  
  fetch('/session-data')
  .then(response => response.json())
  .then(data => {
    if(data.id == null){
      alert('Need To Login')
    }else{
      var userid = data.id

      fetch('/override', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ hydrocode: title, userid: userid, pinNumber: number }),
      })
        .then(response1 => response1.json())
        .then(data => {
          
          if (data.result === 'true') {
            pinLocation(title, number, userid);
          }
          else {
             alert('Cant Pin Location Because need to Override ' + data.Current)
          }
        })
        .catch(error => {
          console.error('Error:', error);
        });
      
      
    
  }
})}

function pinLocation(title,number,userid){
  console.log(userid)
  fetch('/pin-location',
    {
      method:'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({hydrocode:title, userid:userid,pinNumber:number})
    })
}

window.checkpinLocation = checkpinLocation;
