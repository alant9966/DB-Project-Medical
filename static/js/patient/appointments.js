// Calendar functionality
const today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let selectedDay = today.getDate();
let selectedMonth = today.getMonth();
let selectedYear = today.getFullYear();

function renderCalendar() {
    const calendarDays = document.getElementById('calendarDays');
    calendarDays.innerHTML = '';

    // Get first day of month and total days
    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

    // Add empty cells for days before month starts
    for (let i = 0; i < firstDay; i++) {
        const emptyDay = document.createElement('div');
        emptyDay.className = 'calendar-day empty';
        calendarDays.appendChild(emptyDay);
    }

    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
        const dayElement = document.createElement('div');
        dayElement.className = 'calendar-day';
        dayElement.textContent = day;

        // Check if the day is selected
        if (day === selectedDay && currentMonth === selectedMonth && currentYear === selectedYear) {
            dayElement.classList.add('selected');
        }

        dayElement.addEventListener('click', () => {
            // Remove previous selection
            document.querySelectorAll('.calendar-day').forEach(d => {
                d.classList.remove('selected');
            });

            // Add selection to clicked day
            dayElement.classList.add('selected');
            selectedDay = day;
            selectedMonth = currentMonth;
            selectedYear = currentYear;
            updateCurrentDate();

            // Fetch appointments for the selected date
            const selectedDate = formatDate(selectedYear, selectedMonth, selectedDay);
            fetchAppointmentsForDate(selectedDate);
        });

        calendarDays.appendChild(dayElement);
    }
}

function updateCurrentDate() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const currentDateElement = document.querySelector('.current-date');
    if (currentDateElement) {
        currentDateElement.textContent = `${months[selectedMonth]} ${selectedDay}`;
    }
}

function updateYear() {
    const yearElement = document.querySelector('.year');
    if (yearElement) {
        yearElement.textContent = currentYear;
    }
}

// Format date as YYYY-MM-DD
function formatDate(year, month, day) {
    const monthStr = String(month + 1).padStart(2, '0');
    const dayStr = String(day).padStart(2, '0');
    return `${year}-${monthStr}-${dayStr}`;
}

// Format time for display
function formatTime(timeStr) {
    if (!timeStr) return 'N/A';
    try {
        // Handle both "HH:MM:SS" and "HH:MM" formats
        const parts = timeStr.split(':');
        const hours = parseInt(parts[0]);
        const minutes = parseInt(parts[1]);
        const period = hours >= 12 ? 'PM' : 'AM';
        const displayHours = hours % 12 || 12;
        const displayMinutes = String(minutes).padStart(2, '0');
        return `${displayHours}:${displayMinutes} ${period}`;
    } catch (e) {
        return timeStr;
    }
}

// Format date for display
function formatDateDisplay(dateStr) {
    if (!dateStr) return 'N/A';
    try {
        const date = new Date(dateStr + 'T00:00:00');
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
        return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    } catch (e) {
        return dateStr;
    }
}

// Fetch appointments for selected date
async function fetchAppointmentsForDate(date) {
    try {
        const response = await fetch('/patient/appointments-by-date', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ date: date })
        });

        const data = await response.json();
        
        if (data.success) {
            displayAppointments(data.appointments);
        } else {
            console.error('Error fetching appointments:', data.message);
            displayAppointments([]);
        }
    } catch (error) {
        console.error('Error fetching appointments:', error);
        displayAppointments([]);
    }
}

// Display appointments in the list
function displayAppointments(appointments) {
    const appointmentList = document.getElementById('appointmentList');
    
    if (!appointmentList) return;
    
    if (appointments.length === 0) {
        appointmentList.innerHTML = '<div class="no-appointments"><p>No appointments scheduled</p></div>';
    } else {
        appointmentList.innerHTML = appointments.map(appt => {
            const time = formatTime(appt.appointment_time);
            const date = formatDateDisplay(appt.appointment_date);
            const doctorName = `Dr. ${appt.doctor_firstname || ''} ${appt.doctor_lastname || ''}`.trim();
            const room = appt.room_id ? `Room ${appt.room_id}` : 'Room N/A';
            const description = appt.description || 'No description';
            const duration = appt.duration_minutes || 0;
            const appointmentId = appt.appointment_id || appt.id;
            const searchText = `${description} ${appt.doctor_firstname || ''} ${appt.doctor_lastname || ''}`.toLowerCase();
            
            return `
                <div class="appointment-item" data-search="${searchText}" data-appointment-id="${appointmentId}">
                    <div class="appointment-time">
                        ${time} (${duration} min)
                    </div>
                    <div class="appointment-desc">
                        ${description}
                    </div>
                    <div class="appointment-details">
                        <span>${date}</span> •
                        <span>${doctorName}</span> •
                        <span>${room}</span>
                    </div>
                    <div class="appointment-actions">
                        <button class="cancel-appointment-btn" data-appointment-id="${appointmentId}">
                            Cancel Appointment
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }
    initializeSearch();
    initializeCancelButtons();
}

// Initialize search functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    if (!searchInput) return;
    
    // Remove existing event listener
    const newSearchInput = searchInput.cloneNode(true);
    searchInput.parentNode.replaceChild(newSearchInput, searchInput);
    
    newSearchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const appointmentItems = document.querySelectorAll('.appointment-item');
        
        appointmentItems.forEach(item => {
            const searchText = item.getAttribute('data-search');
            if (searchText && searchText.includes(searchTerm)) {
                item.classList.remove('hidden');
            } else {
                item.classList.add('hidden');
            }
        });
    });
}

// Initialize cancel appointment buttons
function initializeCancelButtons() {
    const cancelButtons = document.querySelectorAll('.cancel-appointment-btn');
    
    cancelButtons.forEach(button => {
        // Remove existing event listeners by cloning
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        newButton.addEventListener('click', async (e) => {
            e.stopPropagation();
            const appointmentId = newButton.getAttribute('data-appointment-id');
            
            if (!appointmentId) {
                console.error('Appointment ID not found');
                return;
            }
            
            // Confirm cancellation
            if (!confirm('Are you sure you want to cancel this appointment?')) {
                return;
            }
            
            // Disable button during request
            newButton.disabled = true;
            newButton.textContent = 'Cancelling...';
            
            try {
                const response = await fetch('/patient/appointments/cancel', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ appointment_id: appointmentId })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Refresh the appointment list for the currently selected date
                    const selectedDate = formatDate(selectedYear, selectedMonth, selectedDay);
                    await fetchAppointmentsForDate(selectedDate);
                } else {
                    alert('Error cancelling appointment: ' + (data.message || 'Unknown error'));
                    newButton.disabled = false;
                    newButton.textContent = 'Cancel Appointment';
                }
            } catch (error) {
                console.error('Error cancelling appointment:', error);
                alert('Error cancelling appointment. Please try again.');
                newButton.disabled = false;
                newButton.textContent = 'Cancel Appointment';
            }
        });
    });
}

// Previous month button
document.querySelector('.prev-month').addEventListener('click', () => {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    renderCalendar();
    updateYear();
});

// Next month button
document.querySelector('.next-month').addEventListener('click', () => {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    renderCalendar();
    updateYear();
    // Don't update current date display when navigating months - keep showing selected date
});

// Initialize search functionality
initializeSearch();

// Initialize calendar on page load
renderCalendar();
updateYear();
updateCurrentDate();

// Fetch appointments for current date on page load
fetchAppointmentsForDate(formatDate(currentYear, currentMonth, selectedDay));
