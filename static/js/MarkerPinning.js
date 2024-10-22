/* 
title: MarkerPinning.js

Authors: Vincent Pham

Description: This file contains methods for handling marker Pinning and exporting them into a Database for the dashboard later

Date: 9/7/24
*/

let customerrorPopup;


/* Check whether the location can be pinned or will result in an error */
export function checkpinLocation(title,number){
  
  /*Fetches user information*/
  fetch('/session-data')
  .then(response => response.json())
  .then(data => {
    /*Checks if user is logged in*/
    if(data.id == null){
      alert('Need To Login')
    }else{
      var userid = data.id
      /* Checks whether there is a duplicate ID or if the location is already pinned at the specified number */
      fetch('/override', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ hydrocode: title, userid: userid, pinNumber: number }),
      })
        .then(response1 => response1.json())
        .then(data => {
          /* The location is currently empty and can be pinned */
          if (data.result === 'true') {
            pinLocation(title, number, userid);
          }
          /*The location is currently not empty and can't be pinned */
          else if (data.error==='override'){
             openerrorPopup(data.error,data.override,title,number,userid)

          }
          /* The location has already been pinned at a different number */
          else if(data.error==='dupe'){
            openerrorPopup(data.error,data.dupeLocation,title,number,userid)
          }
          

        })
        .catch(error => {
          console.error('Error:', error);
        });
      
      
    
  }
})}

/* This Function updates the database with new Pinned Location */
function pinLocation(title,number,userid){
  fetch('/pin-location',
    {
      method:'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body:JSON.stringify({hydrocode:title, userid:userid,pinNumber:number})
    })
    closeerrorPopup()
}

/* This Closes the Overlay and errorPopup */
 export function closeerrorPopup(){
  customerrorPopup = document.getElementById('errorpopup');
  customerrorPopup.style.display = 'none';

  document.getElementById('errorpopup').style.visibility = 'hidden'
  document.getElementById('erroroverlay').style.display = 'none';

 }
 /* This Opens the Overlay and errorPopup */
export function openerrorPopup(error,data1,title,number,userid)
{
  document.getElementById('errorpopup').style.visibility = 'visible';
const customerrorPopup = document.getElementById('errorpopup');

// This generates the custom error popup with a message and response buttons
customerrorPopup.innerHTML = `
 <div id="close-error-button" onclick="closeerrorPopup()"><img src="static/images/error-close.svg" alt="Close"></div>
  <div class = "error-content">
    <p>${error === 'override' ? 
    "Override: Are you sure you want to override: " + data1[number] : 
    "Add duplicate (" + title + ")?, it is already pinned to " + data1 + "?"}
</p>
    <div id="error-response-container">
      <button class="error-response-button yes-button" onclick="pinLocation('${title}', '${number}', '${userid}')">Yes</button>
      <button class="error-response-button no-button" onclick="closeerrorPopup()">No</button>
    </div>
  </div>
`;

customerrorPopup.style.display = 'block';
document.getElementById('erroroverlay').style.display = 'block';


}
window.closeerrorPopup= closeerrorPopup
window.pinLocation = pinLocation
window.checkpinLocation = checkpinLocation;
window.openerrorPopup = openerrorPopup
