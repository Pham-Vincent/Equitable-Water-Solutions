/*
  Issue with Circles:
  1.  Need two different circles -> One for Clicking, One for Hovering (Use a set?)
  2.  Radius meaning is not intuitive
*/

//initializes the marker circle to null
export let markerCircle = null;

export function addCircle (map, marker) {
    //When hovering, creates circle of area where marker point exists
    if(markerCircle === null){
        markerCircle = new google.maps.Circle({
            strokeColor: "#FF0000",
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: "#FF0000",
            fillOpacity: 0.35,
            map,
            center: marker.position,
            radius: 1610*2,
          });
    }
  };

export function removeCircle (map, marker) {
    //Hides marker circle from the map and then sets back to null
    if(markerCircle){
      markerCircle.setMap(null);
      markerCircle = null;
    }
  }