function submitGPSForm() {
    const country = document.getElementById('country').value;
    const address = document.getElementById('address').value;
    const itemsNeeded = Array.from(document.querySelectorAll('.form-check-input:checked')).map(input => input.value);
    
    console.log(country);

    // Example of sending data via POST request
    fetch('/GPS', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ country: country, address: address, items: itemsNeeded })
    })
    .then(response => {
        if (response.ok) {
            alert('Submission successful!');
            // Optionally, reset the form or redirect
            document.getElementById('gpsForm').reset();
        } else {
            response.json().then(errorData => {
                alert(`Error during submission: ${errorData.message || 'Unknown error'}`);
            }).catch(() => {
                alert('Error during submission and failed to parse error details.');
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error processing your request.');
    });
}

