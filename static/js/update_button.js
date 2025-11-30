// Wait until the page is fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Handle clicking the "Update" button
    document.querySelectorAll('.update-link').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();  // Prevent the link from navigating
            
            // Retrieve the necessary elements
            const infoRow = this.closest('.info-row');
            const displayValue = infoRow.querySelector('.display-value');
            const editInput = infoRow.querySelector('.edit-input');

            // Swap the visible element
            displayValue.style.display = 'none';
            editInput.style.display = 'inline-block';
            editInput.focus();  // Focus the cursor to the input box
        });
    });

    // Handle pressing "Enter" or "Escape"
    document.querySelectorAll('.edit-input').forEach(input => {
        // Listen for a key press
        input.addEventListener('keyup', function(e) {
            // Save the input on 'Enter'
            if (e.key === 'Enter') {
                saveData(this);
            } 
            
            // Exit the input on 'Escape'
            if (e.key === 'Escape') {
                // Cancel the input
                const infoRow = this.closest('.info-row');
                const displayValue = infoRow.querySelector('.display-value');
                
                // Swap (back) the visible element
                this.style.display = 'none';
                displayValue.style.display = 'inline-block';
                
                // Reset to the original input value
                this.value = displayValue.textContent.trim();
            }
        });
    });

});

// Send the input data to the Flask server
function saveData(inputElement) {
    // Retrieve the relevant elements and data
    const infoRow = inputElement.closest('.info-row');
    const editableValue = inputElement.closest('.edit-value');
    
    const newValue = inputElement.value;
    const fieldName = editableValue.dataset.field;
    
    // Determine if this is a patient or doctor page
    const patientId = infoRow.dataset.patientId;
    const doctorId = infoRow.dataset.doctorId;
    
    let updateUrl;
    let requestBody;
    
    if (patientId) {
        // This is a patient page
        updateUrl = '/patient/update';
        requestBody = {
            patient_id: patientId,
            field: fieldName,
            value: newValue
        };
    } else if (doctorId) {
        // This is a doctor page
        updateUrl = '/doctor/update';
        requestBody = {
            doctor_id: doctorId,
            field: fieldName,
            value: newValue
        };
    } else {
        alert('Error: Could not determine user type. Missing patient_id or doctor_id attribute.');
        return;
    }

    // Send data to Flask using the fetch API
    fetch(updateUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody)
    })
    .then(response => response.json())  // JSON response from Flask
    .then(data => {
        if (data.success) {
            // Update the HTML display
            const displayValue = infoRow.querySelector('.display-value');
            displayValue.textContent = data.new_value;
            
            // Swap (back) the visible element
            inputElement.style.display = 'none';
            displayValue.style.display = 'inline-block';
        } else {
            alert('Error updating: ' + data.message);
        }
    })
    // Handle network errors
    .catch(error => {   
        console.error('Network error:', error);
        alert('A network error occurred. Please try again.');
    });
}