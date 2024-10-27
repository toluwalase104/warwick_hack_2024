// JavaScript for Event Calendar
const monthNames = ["January", "February", "March", "April", "May", "June", 
    "July", "August", "September", "October", "November", "December"];
let currentDate = new Date();
let events = {};

// Function to create the calendar
function createCalendar() {
    const calendar = document.getElementById("calendar");
    const monthYear = document.getElementById("month-year");
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    monthYear.textContent = `${monthNames[month]} ${year}`;
    calendar.innerHTML = ""; // Clear previous days

    // Get the first day of the month
    const firstDay = new Date(year, month, 1);
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Fill in the days
    for (let i = 0; i < firstDay.getDay(); i++) {
        const emptyDiv = document.createElement("div");
        calendar.appendChild(emptyDiv);
    }
    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement("div");
        dayDiv.className = "day";
        dayDiv.textContent = day;
        const dateString = `${year}-${month + 1}-${day}`;

        // Show events if any
        if (events[dateString]) {
            events[dateString].forEach(event => {
                const eventDiv = document.createElement("div");
                eventDiv.className = "event";
                eventDiv.textContent = event.title;
                dayDiv.appendChild(eventDiv);
            });
        }

        // Event listener for adding an event
        dayDiv.addEventListener("click", () => {
            showEventModal(dateString);
        });
        calendar.appendChild(dayDiv);
    }
}

// Function to show event modal
function showEventModal(date) {
    const modal = document.getElementById("event-modal");
    modal.style.display = "block";
    document.getElementById("event-date").value = date; // Set hidden input to date
}

// Close modal functionality
document.querySelector(".close").onclick = function() {
    document.getElementById("event-modal").style.display = "none";
};

// Add event form submission
document.getElementById("event-form").onsubmit = function(event) {
    event.preventDefault();
    const title = document.getElementById("event-title").value;
    const location = document.getElementById("event-location").value;
    const type = document.getElementById("event-type").value;
    const date = document.getElementById("event-date").value;

    if (!events[date]) {
        events[date] = [];
    }
    events[date].push({ title, location, type });
    createCalendar(); // Recreate the calendar to show new event
    document.getElementById("event-modal").style.display = "none";

    // Clear the form fields after submission
    document.getElementById("event-title").value = "";
    document.getElementById("event-location").value = "";
    document.getElementById("event-type").value = ""; // Reset the dropdown
};
// Navigate to previous month
document.getElementById("prev-month").onclick = function() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    createCalendar();
};

// Navigate to next month
document.getElementById("next-month").onclick = function() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    createCalendar();
};

// Initial calendar creation
createCalendar();