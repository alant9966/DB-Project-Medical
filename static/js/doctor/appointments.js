// Function to select an appointment and fetch its details
function selectAppointment(appointmentId) {
    // Remove selected class from all items
    const allItems = document.querySelectorAll('.time-item');
    allItems.forEach(item => {
        item.classList.remove('selected');
    });
    
    // Add selected class to clicked item
    const clickedItem = document.querySelector(`[data-appointment-id="${appointmentId}"]`);
    if (clickedItem) {
        clickedItem.classList.add('selected');
    }
    
    // Fetch appointment details
    fetch(`/doctor/appointments/${appointmentId}/details`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch appointment details');
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update appointment information panel
                updateAppointmentPanel(data.appointment);
                
                // Update patient information panel
                if (data.patient) {
                    updatePatientPanel(data.patient);
                }
                
                // Show both panels
                document.getElementById('appointment-panel').style.display = 'block';
                document.getElementById('patient-panel').style.display = 'block';
            } else {
                console.error('Error:', data.message);
            }
        })
        .catch(error => {
            console.error('Error fetching appointment details:', error);
        });
}

// Function to update appointment information panel
function updateAppointmentPanel(appointment) {
    document.getElementById('appointment-date').textContent = appointment.date || '-';
    document.getElementById('appointment-description').textContent = appointment.description || '-';
    document.getElementById('appointment-duration').textContent = appointment.duration ? appointment.duration + ' minutes' : '-';
    document.getElementById('appointment-patient-id').textContent = appointment.patient_id || '-';
    document.getElementById('appointment-room-id').textContent = appointment.room_id || '-';
}

// Function to update patient information panel
function updatePatientPanel(patient) {
    document.getElementById('patient-id').textContent = patient.id || '-';
    document.getElementById('patient-first-name').textContent = patient.first_name || '-';
    document.getElementById('patient-last-name').textContent = patient.last_name || '-';
    document.getElementById('patient-dob').textContent = patient.dob || '-';
    document.getElementById('patient-weight').textContent = patient.weight ? patient.weight + ' lb' : '-';
    document.getElementById('patient-height').textContent = patient.height ? patient.height + ' in' : '-';
    document.getElementById('patient-age').textContent = patient.age || '-';
    document.getElementById('patient-address').textContent = patient.address || '-';
}

// If an appointment is selected on page load, ensure panels are visible
document.addEventListener('DOMContentLoaded', function() {
    // Check if an appointment has been selected
    const selectedItem = document.querySelector('.time-item.selected');
    if (selectedItem) {
        // Ensure panels are visible
        const appointmentPanel = document.getElementById('appointment-panel');
        const patientPanel = document.getElementById('patient-panel');
        if (appointmentPanel && appointmentPanel.style.display === 'none') {
            appointmentPanel.style.display = 'block';
        }
        if (patientPanel && patientPanel.style.display === 'none') {
            patientPanel.style.display = 'block';
        }
    }
});

