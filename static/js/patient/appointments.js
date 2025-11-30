// Calendar functionality
let currentMonth = 9; // October (0-indexed)
let currentYear = 2025;
let selectedDay = 11;

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

        if (day === selectedDay && currentMonth === 9 && currentYear === 2025) {
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
            updateCurrentDate();
        });

        calendarDays.appendChild(dayElement);
    }
}

function updateCurrentDate() {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const currentDateElement = document.querySelector('.current-date');
    currentDateElement.textContent = `${months[currentMonth]} ${selectedDay}`;
}

function updateYear() {
    const yearElement = document.querySelector('.year');
    yearElement.textContent = currentYear;
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
    updateCurrentDate();
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
    updateCurrentDate();
});

// Calendar action buttons
document.querySelector('.cancel-btn').addEventListener('click', () => {
    // Reset to default selection
    currentMonth = 9;
    currentYear = 2025;
    selectedDay = 11;
    renderCalendar();
    updateYear();
    updateCurrentDate();
});

document.querySelector('.ok-btn').addEventListener('click', () => {
    alert(`Date selected: ${currentMonth + 1}/${selectedDay}/${currentYear}`);
});

// Search functionality
const searchInput = document.getElementById('searchInput');
const appointmentItems = document.querySelectorAll('.appointment-item');

searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();

    appointmentItems.forEach(item => {
        const searchText = item.getAttribute('data-search');
        if (searchText.includes(searchTerm)) {
            item.classList.remove('hidden');
        } else {
            item.classList.add('hidden');
        }
    });
});

// Insurance update links
const updateLinks = document.querySelectorAll('.update-link');

updateLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const fieldName = link.getAttribute('data-field');
        alert(`Update ${fieldName} - This would open a form to update the information.`);
    });
});

// Initialize calendar on page load
renderCalendar();
