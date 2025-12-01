// Wait until the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById('appointment-search');
    const appointmentsList = document.getElementById('appointments-list');
    
    if (!searchInput || !appointmentsList) {
        return;
    }
    
    // Store the original appointment's HTML for resetting
    const originalAppointmentsHTML = appointmentsList.innerHTML;
    
    // Handle pressing the Enter key
    searchInput.addEventListener('keyup', function(e) {
        if (e.key === 'Enter') {
            performSearch(this.value);
        }
    });
    
    // Handle clearing search (show all when empty)
    searchInput.addEventListener('input', function(e) {
        if (this.value.trim() === '') {
            resetAppointments();
        }
    });
    
    function performSearch(query) {
        const searchQuery = query.trim();
        
        // If empty query, reset to show all
        if (searchQuery === '') {
            resetAppointments();
            return;
        }
        
        // Send search request to server
        fetch('/patient/search-appointments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: searchQuery })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayAppointments(data.appointments);
            } else {
                alert('Error searching appointments: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Network error:', error);
            alert('A network error occurred. Please try again.');
        });
    }
    
    function displayAppointments(appointments) {
        if (appointments.length === 0) {
            appointmentsList.innerHTML = '<p>No appointments found matching your search.</p>';
            return;
        }
        
        let html = '';
        appointments.forEach(appt => {
            const date = new Date(appt.appointment_date);
            const time = formatTime(appt.appointment_time);
            const dateFormatted = formatDate(date);
            
            html += `
                <div class="appointment-item">
                    <div class="appointment-date">
                        <strong>${dateFormatted}</strong>
                    </div>
                    <div class="appointment-details">
                        <span class="time">${time}</span>
                        <span class="description">${appt.description}</span>
                    </div>
                </div>
            `;
        });
        
        appointmentsList.innerHTML = html;
    }
    
    function resetAppointments() {
        appointmentsList.innerHTML = originalAppointmentsHTML;
    }
    
    function formatDate(date) {
        const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        
        const dayName = days[date.getDay()];
        const month = months[date.getMonth()];
        const day = date.getDate();
        
        return `${dayName}, ${month} ${day}`;
    }
    
    function formatTime(timeString) {
        if (!timeString) return '';
        
        // Parse time string (HH:MM:SS or HH:MM)
        const parts = timeString.split(':');
        const hours = parseInt(parts[0], 10);
        const minutes = parts[1];
        
        const period = hours >= 12 ? 'PM' : 'AM';
        const displayHours = hours % 12 || 12;
        
        return `${displayHours}:${minutes} ${period}`;
    }
});

