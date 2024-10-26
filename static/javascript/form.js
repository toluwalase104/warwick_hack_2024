// Function to display the role selection after filling in personal details
function showRoleSelection() {
    document.getElementById('personalDetails').style.display = 'none';
    document.getElementById('roleSelection').style.display = 'block';
}

// Function to display resource options based on the selected role
function showOptions(role) {
    document.getElementById('roleSelection').style.display = 'none';
    document.getElementById('options').style.display = 'block';

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

    // Capture the description as a separate field
    const description = document.getElementById('description').value.trim();

    // Construct the data object to be sent to the server
    const formData = {
        name: name,
        contact: contact,
        address: address,
        postcode: postcode,
        role: role,
        options: options,
        description: description // Include description as a separate field
    };

    // Send data to the server at the correct endpoint
    fetch('/resourceRequests', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Log the response data for debugging
        alert('Form submitted successfully!');
        document.getElementById('mainForm').reset(); // Reset the form
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was a problem submitting the form.');
    });
};


