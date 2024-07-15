import React, { useEffect, useRef, useState } from 'react';
import config from './../js/config.js';

const MapComponent = () => {
  const mapRef = useRef(null);
  const popupRef = useRef(null);
  const overlayRef = useRef(null);
  const [map, setMap] = useState(null);

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

    const allowedBounds = new google.maps.LatLngBounds(
      new google.maps.LatLng(-60, -180),
      new google.maps.LatLng(85, 180)
    );

    const mapInstance = new Map(mapRef.current, {
      center: { lat: 38.2, lng: -76.2 },
      zoom: 8.2,
      mapId: "366d3e13ce470bd7",
      scrollwheel: true,
      streetViewControl: false,
      fullscreenControl: false,
      mapTypeControl: false,
      restriction: {
        latLngBounds: allowedBounds,
        strictBounds: false
      }
    });

    mapInstance.data.loadGeoJson('json/Chesapeake_Bay_Shoreline_High_Resolution.geojson');

    mapInstance.data.setStyle({
      fillColor: '#5a5fcf',
      fillOpacity: .4,
      strokeWeight: 0,
    });

    mapInstance.setOptions({ minZoom: 3 });

    try {
      const response = await fetch('json/VA_final_v3.json', {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();

      data.forEach(point => {
        const mapCode = point.Hydrocode;
        const desc1 = point.Source_Type;
        const locality = point.Locality;

        const newMarker = new google.maps.Marker({
          position: { lat: parseFloat(point.Latitude), lng: parseFloat(point.Longitude) },
          map: mapInstance,
          title: mapCode,
        });

        const infowindow = new InfoWindow({
          content: `
            <div class="info-window">
              <strong>${newMarker.title}</strong>
              <p>${desc1}</p>
              <p>${locality}</p>
            </div>
          `,
          maxWidth: 300,
        });

        newMarker.addListener('mouseover', () => {
          infowindow.open(mapInstance, newMarker);
        });

        newMarker.addListener('mouseout', () => {
          infowindow.close();
        });

        newMarker.addListener("click", () => {
          popUpLayer1(newMarker);
          infowindow.close();
        });
      });

    } catch (error) {
      console.error('Error fetching or processing data:', error);
    }

    setMap(mapInstance);
  };

  const popUpLayer1 = (marker) => {
    if (window.smallInfowindow) {
      window.smallInfowindow.close();
    }

    const infowindow = new google.maps.InfoWindow({
      content: `
        <div class="info-window">
          <strong>${marker.getTitle()}</strong>
          <p>${marker.getTitle()}</p>
        </div>
      `,
      maxWidth: 300,
    });

    infowindow.open(map, marker);
    window.smallInfowindow = infowindow;
  };

  const closePopup = () => {
    const popup = popupRef.current;
    if (popup) {
      popup.style.display = 'none';
    }
    const overlay = overlayRef.current;
    if (overlay) {
      overlay.style.display = 'none';
    }
  };

  useEffect(() => {
    Load_Map();
    initMap();
  }, []);

  useEffect(() => {
    const overlay = overlayRef.current;
    if (overlay) {
      overlay.addEventListener('click', closePopup);
    }

    return () => {
      if (overlay) {
        overlay.removeEventListener('click', closePopup);
      }
    };
  }, []);

  return (
    <div>
      <div id="map" ref={mapRef} style={{ width: '100%', height: '100vh' }}></div>
      <div id="popup" ref={popupRef} style={{ display: 'none' }}></div>
      <div id="overlay" ref={overlayRef} style={{ display: 'none' }}></div>
    </div>
  );
};

export default MapComponent;
