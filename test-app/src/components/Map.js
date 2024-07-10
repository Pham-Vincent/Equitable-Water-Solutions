import React, { useEffect, useRef, useState } from 'react';
import config from './../js/config.js';


const MapComponent = () => {
  const mapRef = useRef(null);
  const [map, setMap] = useState(null);
  const [markers, setMarkers] = useState([]);
  const [customPopup, setCustomPopup] = useState(null);

  const Load_Map = () => {
    (g => {
      var h, a, k, p = "The Google Maps JavaScript API", c = "google", l = "importLibrary", q = "__ib__", m = document, b = window;
      b = b[c] || (b[c] = {});
      var d = b.maps || (b.maps = {}), r = new Set, e = new URLSearchParams;

      const loadScript = async () => {
        await (a = m.createElement("script"));
        e.set("libraries", [...r] + "places");
        for (k in g) e.set(k.replace(/[A-Z]/g, t => "_" + t[0].toLowerCase()), g[k]);
        e.set("callback", c + ".maps." + q);
        a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
        return new Promise((resolve, reject) => {
          d[q] = resolve;
          a.onerror = () => reject(Error(p + " could not load."));
          a.nonce = m.querySelector("script[nonce]")?.nonce || "";
          m.head.append(a);
        });
      };

      const u = () => h || (h = loadScript());
      d[l] ? console.warn(p + " only loads once. Ignoring:", g) : d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n));
    })({ key: config.apiKey, v: "weekly" });
  };

  const initMap = async () => {
    await Load_Map();
    const { Map, InfoWindow } = await google.maps.importLibrary("maps");
    let markersList = [];

    const allowedBounds = new google.maps.LatLngBounds(
        new google.maps.LatLng(-60, -180),// Southwest corner (60 degrees south, entire western hemisphere)
        new google.maps.LatLng(85, 180) // Northeast corner (North Pole, entire eastern hemisphere)
      );

    const mapInstance = new Map(mapRef.current, {
        center: { lat: 38.2, lng: -76.2 },
        zoom: 8.2,
      
        //Mappitng Styles:
        //366d3e13ce470bd7 -> No Background Signs/Feature Styling Disabled
        //45c77a2db5a260c8 -> Background Signs/Feature Styling Enabled
        mapId: "366d3e13ce470bd7", 
        scrollwheel:true, //bypasses command+scroll to zoom
        streetViewControl: false, //removes streetview pegman
        fullscreenControl: false, //removes fullscreen button
        mapTypeControl: false, //removes map type buttons (terrian/satellite)
        restriction: {
          latLngBounds: allowedBounds,// Gives the Maps Boundaries 
          strictBounds: false // Set to true if you want to completely restrict panning
        }
    });

    //Loads GeoJSON Data from JSON file
    mapInstance.data.loadGeoJson('json/Chesapeake_Bay_Shoreline_High_Resolution.geojson');

    //Changes The Styling Within Map Boundaries
    mapInstance.data.setStyle({
        fillColor: '#5a5fcf', //blue
        fillOpacity : .4,
        strokeWeight: 0,
    });
    /* Sets the Maximum Zoom out Value */
  mapInstance.setOptions({ minZoom: 3});

    console.log("Fetch request started");

    try {
      const response = await fetch('json/Va_Permit.json', {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      console.log("Fetch request completed successfully");

      const loadedMarkers = data.map(point => {
        const mapCode = point.Hydrocode;
        const desc1 = point.Source_Type;
        const latitude = parseFloat(point.Latitude);
        const longitude = parseFloat(point.Longitude);
        const locality = point.Locality;

        const marker = new google.maps.Marker({
          position: { lat: latitude, lng: longitude },
          map: mapInstance,
          title: mapCode,
          descriptions: {
            description1: desc1,
            description2: locality
          },
          points: {
            point1: parseFloat(point.Year_2016),
            point2: parseFloat(point.Year_2017),
            point3: parseFloat(point.Year_2018),
            point4: parseFloat(point.Year_2019),
            point5: parseFloat(point.Year_2020)
          }
        });

        markersList.push(marker);

        const infowindow = new InfoWindow({
          content: `
            <div class="info-window">
              <strong>${marker.title}</strong>
            </div>
          `,
          maxWidth: 300,
        });

        marker.addListener('mouseover', () => {
          if (!window.popupLayerOpen) {
            infowindow.open(mapInstance, marker);
          }
        });

        marker.addListener('mouseout', () => {
          if (!window.popupLayerOpen) {
            infowindow.close();
          }
        });

        marker.addListener("click", () => {
          popUpLayer1(marker);
          infowindow.close();
          window.popupLayerOpen = true;
        });

        return marker;
      });

      setMarkers(loadedMarkers);
    } catch (error) {
      console.error('Error:', error);
    }

    setMap(mapInstance);
  };

  const popUpLayer1 = (marker) => {
    if (window.smallInfowindow) {
      window.smallInfowindow.close();
    }

    const popupTitle = marker.getTitle();

    const smallInfowindow = new google.maps.InfoWindow({
      content: `
        <div class="info-window">
          <strong>${marker.getTitle()}</strong>
          <p>${marker.descriptions.description1}</p>
          <p>${marker.descriptions.description2}</p>
          <button id="view-more-button" onclick="viewMore('${marker.graph}')">View More</button>
        </div>
      `,
      maxWidth: 300,
    });

    google.maps.event.addListener(map, 'click', function () {
      smallInfowindow.close();
      window.popupLayerOpen = false;
    });

    smallInfowindow.open(map, marker);
    window.smallInfowindow = smallInfowindow;
    window.popupTitle = popupTitle;

    smallInfowindow.addListener('closeclick', () => {
      window.popupLayerOpen = false;
    });
  };

  //Function to handle the view more button
  function viewMore(currentGraph) {
  window.smallInfowindow.close();
  openPopup(window.currentMarker, currentGraph);
}

  const openPopup = (marker, currentGraph) => {
    const popup = document.getElementById('popup');
    popup.innerHTML = `
      <h1>${marker.getTitle()}</h1>
      <div class="info-window">
        <p>${marker.descriptions.description1}</p>
        <p>${marker.descriptions.description2}</p>
        <div id="close-button" onclick="closePopup()">X</div>
      </div>
    `;
    popup.style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
    setCustomPopup(popup);
  };

  const closePopup = () => {
    customPopup.style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
  };

  const handleKeyPress = (event) => {
    if (event.keyCode === 13) {
      const searchInput = document.getElementById("search-input").value.trim();
      if (searchInput !== "") {
        search();
      }
    }
  };

  const search = () => {
    const searchInput = document.getElementById("search-input").value.toLowerCase();

    markers.forEach(marker => {
      const markerTitle = marker.getTitle().toLowerCase();

      if (markerTitle.includes(searchInput)) {
        console.log("Match found!");
        openPopup(marker, marker.graph);
      } else {
        console.log("Not found");
      }
    });
  };

  useEffect(() => {
    Load_Map();
    initMap();
  }, []);

  useEffect(() => {
    document.getElementById('overlay').addEventListener('click', viewMore);
    document.getElementById('overlay').addEventListener('click', closePopup);
    document.getElementById("search-input").addEventListener("keypress", handleKeyPress);
  }, []);

  return (
    <div>
      <div id="map" ref={mapRef} style={{ width: '100%', height: '100vh' }}></div>
      <div id="popup" style={{ display: 'none' }}></div>
      <div id="overlay" style={{ display: 'none' }}></div>
      <input type="text" id="search-input" placeholder="Search..." />
    </div>
  );
};

export default MapComponent;
