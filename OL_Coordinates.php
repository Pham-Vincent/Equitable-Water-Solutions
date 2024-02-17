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

        /* Styling for the custom popup */
        .popup {
            display: none;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            padding: 20px;
            border-radius: 5px;
            z-index: 1000;
            width: 50%; /* Set width to 50% */
            max-width: 600px; /* Set maximum width */
        }

        .popup-content {
            text-align: center;
        }

        .popup-close {
            position: absolute;
            top: 5px;
            right: 5px;
            cursor: pointer;
        }
    </style>
</head>
<body style="height: 100%;">
    <div id="map"></div>

    <!-- Custom popup HTML -->
    <div id="popup" class="popup">
        <span class="popup-close" onclick="closePopup()">&times;</span>
        <div class="popup-content">
            <h2 id="popup-title"></h2>
            <div id="popup-body"></div>
        </div>
    </div>

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
        function addMarker(lon, lat, name, imageUrl, description) {
            var marker = new ol.Feature({
                geometry: new ol.geom.Point(ol.proj.fromLonLat([lon, lat])),
                name: name,
                imageUrl: imageUrl,
                description: description
            });

            vectorLayer.getSource().addFeature(marker);
        }

        // Add markers for specific points
        addMarker(-73.9857, 40.7484, "New York City", "https://via.placeholder.com/150", "This is New York City."); // Example coordinates for New York City
        addMarker(-0.1276, 51.5074, "London", "https://via.placeholder.com/150", "This is London.");  // Example coordinates for London
	    addMarker(-77.268023, 38.581805, "Powell Creek", "https://via.placeholder.com/150", "This is Powell Creek.");
	    addMarker(-77.3365718, 38.6036475, "Lake Montclair", "https://via.placeholder.com/150", "This is Lake Montclair.");
    	addMarker(-77.47041, 38.444518, "Pond", "https://via.placeholder.com/150", "This is Pond.");
    	addMarker(-76.98545, 38.14749, "Walnut Hill", "https://via.placeholder.com/150", "This is Walnut Hill.");
    	addMarker(-76.71816392, 38.0831967, "FARM POND #1 (LARGE)", "https://via.placeholder.com/150", "This is FARM POND #1 (LARGE).");


        // Custom popup element
        var popup = document.getElementById('popup');
        var popupTitle = document.getElementById('popup-title');
        var popupBody = document.getElementById('popup-body');

        // Event listener to handle when a marker is clicked
        map.on('click', function (event) {
            var feature = map.forEachFeatureAtPixel(event.pixel, function (feature, layer) {
                return feature;
            });

            if (feature) {
                var coordinate = feature.getGeometry().getCoordinates();
                var name = feature.get('name');
                var imageUrl = feature.get('imageUrl');
                var description = feature.get('description');

                // Set popup content
                popupTitle.innerHTML = name;
                popupBody.innerHTML = '<img src="' + imageUrl + '"/><p>' + description + '</p>';

                // Show popup
                popup.style.display = 'block';
            } else {
                popup.style.display = 'none';
            }
        });

        // Function to close the popup
        function closePopup() {
            popup.style.display = 'none';
        }
    </script>
</body>
</html>
