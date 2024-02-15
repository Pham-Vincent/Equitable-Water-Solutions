<!DOCTYPE html>
<html lang="en" style="height: 100%;">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OpenLayers Map</title>
    <!-- Include OpenLayers library -->
    <link rel="stylesheet" href="https://openlayers.org/en/v6.13.0/css/ol.css" type="text/css">
    <script src="https://openlayers.org/en/v6.13.0/build/ol.js"></script>
    <style>
        html, body, #map {
            height: 100%;
            margin: 0;
            padding: 0;
        }
    </style>
</head>
<body style="height: 100%;">
    <div id="map"></div>

    <script>
        // Create a map
        var map = new ol.Map({
            target: 'map', // The id of the div containing the map
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM() // OpenStreetMap layer
                })
            ],
            view: new ol.View({
                center: ol.proj.fromLonLat([0, 0]), // Center coordinates in LonLat projection
                zoom: 2 // Initial zoom level
            })
        });

        // Create a vector layer to hold the markers
        var vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector()
        });

        // Add the vector layer to the map
        map.addLayer(vectorLayer);

        // Function to add a marker to the map
        function addMarker(lon, lat) {
            var marker = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat]))
            });
            vectorLayer.getSource().addFeature(marker);
        }

        // Add markers for specific points
        addMarker(-73.9857, 40.7484); // Example coordinates for New York City
        addMarker(-0.1276, 51.5074);  // Example coordinates for London
    </script>
</body>
</html>
