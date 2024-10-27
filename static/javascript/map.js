function showMapWithLocations() {
    // Reveal the map container
    document.getElementById('map').style.display = 'block';

    // Initialize Leaflet map
    let map = L.map('map').setView([43.1061288, -79.0736703], 12);  // Default location
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    // Fetch location data from google_places.txt
    fetch('/static/google_places.txt')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.text();
        })
        .then(data => {
            const locations = parseLocationData(data);
            placeMarkers(locations, map);
        })
        .catch(error => console.error('Error fetching locations:', error));
}

// Parse the location data from google_places.txt
function parseLocationData(data) {
    const locations = [];
    const lines = data.trim().split('\n');
    for (const line of lines) {
        const [name, lat, lng] = line.split('\t');
        if (name && lat && lng) {
            locations.push({
                name: name.trim(),
                lat: parseFloat(lat),
                lng: parseFloat(lng)
            });
        }
    }
    return locations;
}

// Place markers on the map for each location with a custom blue icon
function placeMarkers(locations, map) {
    const blueIcon = L.icon({
        iconUrl: 'https://upload.wikimedia.org/wikipedia/commons/3/3f/Marker.png', // URL to a blue marker icon
        iconSize: [25, 41], // Size of the icon
        iconAnchor: [12, 41], // Point of the icon which will correspond to marker's location
        popupAnchor: [1, -34], // Point from which the popup should open relative to the iconAnchor
    });

    const markers = locations.map(location => {
        const marker = L.marker([location.lat, location.lng], { icon: blueIcon }).addTo(map);
        marker.bindPopup(`<strong>${location.name}</strong>`);
        return marker;
    });

    // Adjust map view to fit all markers
    if (markers.length > 0) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds());
    }
}
