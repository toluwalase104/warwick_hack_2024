function submitGPSForm() {
    const country = document.getElementById('country').value;
    const address = document.getElementById('address').value;
    const itemsNeeded = Array.from(document.querySelectorAll('.form-check-input:checked')).map(input => input.value);
    
    // Log user input
    console.log("Country:", country);
    console.log("Address:", address);
    console.log("Items Needed:", itemsNeeded);

    // Fetch the places data and display locations
    fetchPlacesData();
}

// Function to fetch places data from google_places.txt
function fetchPlacesData() {
    fetch('./google_places.txt')  // Adjust the path as necessary
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();  // Parse the response as text
        })
        .then(data => {
            // Process the fetched data and display locations
            displayPlaces(data);
        })
        .catch(error => {
            console.error('There has been a problem with your fetch operation:', error);
        });
}

// Function to display places in the HTML
function displayPlaces(placesData) {
    const locationsContainer = document.getElementById('locations');
    locationsContainer.innerHTML = '';  // Clear previous locations

    const title = document.createElement('h3');
    title.innerText = "Nearby Places:";
    locationsContainer.appendChild(title);

    const list = document.createElement('ul');
    list.style.listStyleType = 'none';  // Remove bullet points
    list.style.textAlign = 'center';     // Center the text

    const places = parseLocationData(placesData);  // Use the fetched data
    places.forEach(place => {
        const listItem = document.createElement('li');
        listItem.innerText = place.name;  // Set the place name
        listItem.style.margin = '5px 0';  // Add vertical spacing
        list.appendChild(listItem);
    });
    
    locationsContainer.appendChild(list);

    // Hide the form and show locations
    document.getElementById('gpsForm').style.display = 'none';  // Hide the form
    locationsContainer.style.display = 'block';  // Show the locations
}

// Parse the location data from the fetched google_places.txt content
function parseLocationData(data) {
    const locations = [];
    const lines = data.trim().split('\n');
    for (const line of lines) {
        const [name] = line.split('\t');  // Only take the name
        if (name) {
            locations.push({ name: name.trim() });  // Store as object if you need to expand later
        }
    }
    return locations;
}

