// Function to display the role selection after filling in personal details
function showRoleSelection() {
    // Hide personal details section
    document.getElementById('personalDetails').style.display = 'none';
    // Show the role selection buttons
    document.getElementById('roleSelection').style.display = 'block';
}

// Function to display resource options based on the selected role
function showOptions(role) {
    // Hide role selection section
    document.getElementById('roleSelection').style.display = 'none';
    // Show the options for resources
    document.getElementById('options').style.display = 'block';

    // Store the selected role in a custom data attribute of the form
    const form = document.getElementById('mainForm');
    form.setAttribute('data-role', role);
}

// Attach an event listener to handle form submission
document.getElementById('mainForm').onsubmit = function (event) {
    event.preventDefault(); // Prevent default form submission

    // Capture personal details from the form
    const name = document.getElementById('name').value;
    const contact = document.getElementById('contact').value;
    const address = document.getElementById('address').value;
    const postcode = document.getElementById('postcode').value;
    const role = this.getAttribute('data-role'); // Get selected role

    // Capture selected options
    const options = Array.from(document.querySelectorAll('#options input:checked')).map(input => input.value);

    // Construct the data object to be sent to the server
    const formData = {
        name: name,
        contact: contact,
        address: address,
        postcode: postcode,
        role: role,
        options: options
    };

    // Send data to the server at the correct endpoint
    fetch('/resourceRequests', { // Endpoint to which data is sent
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' // Specify the content type
        },
        body: JSON.stringify(formData) // Convert the data object to JSON
    })
    .then(response => {
        if (!response.ok) { // Check if the response is okay
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse JSON response
    })
    .then(data => {
        console.log(data); // Log the response data for debugging
        alert('Form submitted successfully!'); // Show a success message
        document.getElementById('mainForm').reset(); // Reset the form
    })
    .catch(error => {
        console.error('Error:', error); // Log any errors
        alert('There was a problem submitting the form.'); // Show error message
    });
};

