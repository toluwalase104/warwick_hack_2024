// List of countries
const countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", 
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", 
    "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", 
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", 
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", 
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", 
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", 
    "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", 
    "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", 
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", 
    "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", 
    "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", 
    "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", 
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", 
    "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", 
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", 
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", 
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", 
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", 
    "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", 
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", 
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", 
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", 
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", 
    "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", 
    "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", 
    "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", 
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", 
    "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", 
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
];

// Populate the dropdown with country options
const countryDropdown = document.getElementById('countryDropdown');

countries.forEach(country => {
    const option = document.createElement('div');
    option.classList.add('dropdown-item');
    option.innerText = country;
    option.onclick = function () {
        document.getElementById('country').value = country; // Set the input value
        countryDropdown.style.display = 'none'; // Hide dropdown after selection
    };
    countryDropdown.appendChild(option);
});

// Function to filter countries based on user input
function filterCountries() {
    const input = document.getElementById('country').value.toLowerCase();
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    let hasVisibleItems = false; // Track if any items are visible

    dropdownItems.forEach(item => {
        if (item.innerText.toLowerCase().includes(input) && input !== "") {
            item.style.display = 'block';
            hasVisibleItems = true; // At least one item is visible
        } else {
            item.style.display = 'none';
        }
    });

    // Show or hide the dropdown based on visibility of items
    countryDropdown.style.display = hasVisibleItems ? 'block' : 'none';
}

// Hide the dropdown if clicked outside
document.addEventListener('click', function(event) {
    if (!document.querySelector('.dropdown').contains(event.target)) {
        countryDropdown.style.display = 'none';
    }
});
