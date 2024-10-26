function submitGPSForm() {
    const country = document.getElementById('country').value;
    const address = document.getElementById('address').value;
    const itemsNeeded = Array.from(document.querySelectorAll('.form-check-input:checked')).map(input => input.value);
    
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
            alert('Error during submission.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error processing your request.');
    });
}

