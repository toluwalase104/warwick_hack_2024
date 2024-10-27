// Sample data to simulate the google_places.txt content
const placesData = `
St Vincent De Paul Society Niagara Falls\t43.1061288\t-79.0736703
GROW Community Food Literacy Centre\t43.11034069999999\t-79.07900769999999
Holy Family Jesus Mary Food Pantry\t43.0952543\t-79.0455704
Community Missions - Food Distribution Center\t43.0830493\t-79.0432402
Heart, Love and Soul\t43.10839480000001\t-79.05287849999999
Magdalene Project Soup Kitchen - Food Distribution Center\t43.0870647\t-79.0386784
Niagara Community Church\t43.0949001\t-79.083117
Niagara Falls Soup Kitchen\t43.1036914\t-79.0703552
Project SHARE\t43.1137302\t-79.0867572
Niagara County Food Distribution\t43.0949224\t-79.0354636
Rose Marra Center\t43.0933511\t-79.039099
Divine Mercy Food Pantry - Food Distribution Center\t43.0881047\t-79.0324175
Community Missions Inc\t43.0830484\t-79.043264
ATM (Star Food Mart)\t43.0894475\t-79.0623231
Saint Joseph Outreach - Food Distribution Center\t43.0943184\t-79.04477779999999
Hearts for the Homeless\t43.1082761\t-79.0297367
Niagara Worship Centre\t43.0939577\t-79.1096091
First United Methodist Church - Food Distribution Center\t43.07568320000001\t-78.969956
Community Care Food Bank\t43.1247806\t-79.2027006
Big Mike's Roosevelt Street Little Food Pantry\t43.0105783\t-78.8754821
`.trim();

function submitGPSForm() {
    const country = document.getElementById('country').value;
    const address = document.getElementById('address').value;
    const itemsNeeded = Array.from(document.querySelectorAll('.form-check-input:checked')).map(input => input.value);
    
    // You can add logic to save this data if needed, or just log it
    console.log("Country:", country);
    console.log("Address:", address);
    console.log("Items Needed:", itemsNeeded);

    // Process the "file" and display locations
    displayPlaces();
}

// Function to display places in the HTML
function displayPlaces() {
    const locationsContainer = document.getElementById('locations');
    locationsContainer.innerHTML = '';  // Clear previous locations

    const title = document.createElement('h3');
    title.innerText = "Nearby Places:";
    locationsContainer.appendChild(title);

    const list = document.createElement('ul');

    const places = parseLocationData(placesData);  // Use the simulated data
    places.forEach(place => {
        const listItem = document.createElement('li');
        listItem.innerText = place.name;  // Set the place name
        list.appendChild(listItem);
    });
    
    locationsContainer.appendChild(list);

    // Hide the form and show locations
    document.getElementById('gpsForm').style.display = 'none';  // Hide the form
    locationsContainer.style.display = 'block';  // Show the locations
}

// Parse the location data from the simulated google_places.txt content
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
