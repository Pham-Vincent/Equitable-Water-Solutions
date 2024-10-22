/* 
title: MarkerPinning.js

Authors: Vincent Pham

Description: This file contains methods for handling marker Pinning and exporting them into a Database for the dashboard later

Date: 9/7/24
*/

let customerrorPopup;

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
          else if (data.error==='override'){
             //alert('Cant Pin Location Because need to Override ' + data.override)
             openerrorPopup(data.error,data.override,title,number,userid)

          }
          else if(data.error==='dupe'){
            openerrorPopup(data.error,data.dupeLocation,title,number,userid)
          }
          

        })
        .catch(error => {
          console.error('Error:', error);
        });
      
      
    
  }
})}

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


 function closeerrorPopup(){
  customerrorPopup = document.getElementById('errorpopup');
  customerrorPopup.style.display = 'none';

  document.getElementById('errorpopup').style.visibility = 'hidden'
  document.getElementById('erroroverlay').style.display = 'none';

 }
export function openerrorPopup(error,data1,title,number,userid)
{
  console.log(data1)
  document.getElementById('errorpopup').style.visibility = 'visible';
const customerrorPopup = document.getElementById('errorpopup');

customerrorPopup.innerHTML = `
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
