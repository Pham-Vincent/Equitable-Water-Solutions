/* 
title: search.js

Authors: William Lamuth, Vincent Pham

Description: This file contains functions for handling the search bar functionality in the application. 
It exports autocomplete,to scriptjs. The autocomplete() function is responsible for creating a container.
This container will display markers that match with what is currently being searched. This Autocomplete search feature
will call search(). If a match is found, it zooms and centers the map on the matching marker's position and opens an info window to highlight the marker. 

Date: 05/05/24
*/
import { shown } from './script.js';


export function search(markers, map) {
    //Looks inside the input box and gets value inside 
    const searchInput = document.getElementById("search-input").value.trim().toLowerCase();
    //It will only open the first marker found 
    let matchfound=false;

    //Looks at Each marker to compare input
    markers.forEach(marker => {
      
      //Changes marker to lowercase to compare with Searchinput 
      const markerTitle = marker.title.toLowerCase();
      //currently zooms and centers on marker. opens infowindow to highlight
      if (markerTitle.includes(searchInput) && !matchfound) {
        map.panTo(marker.position);
        map.setZoom(20);
        const infowindow = marker.infowindow; //Find the infowindow associated with the marker
        openInfoWindow2(marker, map, infowindow); 
        //When Finds a Map it won't search anymore
        matchfound = true
        return;
      }
      });
      
 
  } 


export function autocomplete(inp, arr,map) {
 
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  //Listens For any inputs in searchbox
  inp.addEventListener("input", function(){
    var a,b,i,val = this.value;
    closeAllLists();
    if(!val){return false;}

    currentFocus = -1;
    a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].title.substr(0, val.length).toUpperCase() == val.toUpperCase() && arr[i].descriptions.visible == shown[1]) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].title.substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].title.substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i].title + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
              //Searches the map
              search(arr,map)
              
          });
          a.appendChild(b);
        }
      }

  })
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    const autocompletelist = document.querySelector(".autocomplete-items");

    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
      increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
      
    } else if (e.keyCode == 38) { //up
      /*If the arrow UP key is pressed,
      decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
      search(arr,map)
      
    }

    //Only will Scroll to the nearest block when hitting Arrow Keys or Enter
    if(e.keyCode == 38 || e.keyCode == 40)
      {
      if(currentFocus != -1)
        {
        const focusedItem = x[currentFocus];

          // Scroll to the position of the currently focused item
          if (focusedItem) {
              focusedItem.scrollIntoView({
                  block: 'nearest'
              });
            }
      }
      }
});
function addActive(x) {
  /*a function to classify an item as "active":*/
  if (!x) return false;
  /*start by removing the "active" class on all items:*/
  removeActive(x);
  if (currentFocus >= x.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = (x.length - 1);
  /*add class "autocomplete-active":*/
  x[currentFocus].classList.add("autocomplete-active");
}
function removeActive(x) {
  /*a function to remove the "active" class from all autocomplete items:*/
  for (var i = 0; i < x.length; i++) {
    x[i].classList.remove("autocomplete-active");
  }
}
function closeAllLists(elmnt) {
  /*close all autocomplete lists in the document,
  except the one passed as an argument:*/
  var x = document.getElementsByClassName("autocomplete-items");
  for (var i = 0; i < x.length; i++) {
    if (elmnt != x[i] && elmnt != inp) {
    x[i].parentNode.removeChild(x[i]);
  }
}
}

/*execute a function when someone clicks in the document:*/
document.addEventListener("click", function (e) {
  closeAllLists(e.target);
});

}

  