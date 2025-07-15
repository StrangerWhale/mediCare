// Main JavaScript for mediCare

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Appointment booking functionality
    const appointmentForm = document.getElementById('appointment-form');
    if (appointmentForm) {
        const dateInput = document.getElementById('id_appointment_date');
        const timeSelect = document.getElementById('time-slots');
        const doctorId = appointmentForm.dataset.doctorId;

        if (dateInput && timeSelect) {
            dateInput.addEventListener('change', function() {
                const selectedDate = this.value;
                if (selectedDate) {
                    loadAvailableSlots(doctorId, selectedDate);
                }
            });
        }
    }

    // Time slot selection
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('time-slot')) {
            // Remove selected class from all slots
            document.querySelectorAll('.time-slot').forEach(slot => {
                slot.classList.remove('selected', 'btn-success');
                slot.classList.add('btn-outline-primary');
            });
            
            // Add selected class to clicked slot
            e.target.classList.remove('btn-outline-primary');
            e.target.classList.add('selected', 'btn-success');
            
            // Update hidden time input
            const timeInput = document.getElementById('id_appointment_time');
            if (timeInput) {
                timeInput.value = e.target.dataset.time;
            }
        }
    });

    // Search functionality
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        const searchInput = document.getElementById('search-input');
        const specializationSelect = document.getElementById('specialization-select');
        
        // Auto-submit form on specialization change
        if (specializationSelect) {
            specializationSelect.addEventListener('change', function() {
                searchForm.submit();
            });
        }
    }

    // Confirmation dialogs
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('confirm-action')) {
            const action = e.target.dataset.action || 'perform this action';
            if (!confirm(`Are you sure you want to ${action}?`)) {
                e.preventDefault();
            }
        }
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Load available time slots for appointment booking
function loadAvailableSlots(doctorId, date) {
    const timeSlotsContainer = document.getElementById('time-slots');
    if (!timeSlotsContainer) return;

    // Show loading
    timeSlotsContainer.innerHTML = '<div class="text-center"><div class="loading"></div> Loading available slots...</div>';

    fetch(`/appointments/available-slots/${doctorId}/${date}/`)
        .then(response => response.json())
        .then(data => {
            if (data.slots && data.slots.length > 0) {
                let slotsHtml = '<h6 class="mb-3">Available Time Slots:</h6><div class="row">';
                data.slots.forEach(slot => {
                    slotsHtml += `
                        <div class="col-md-3 col-sm-4 col-6 mb-2">
                            <button type="button" class="btn btn-outline-primary btn-sm time-slot w-100" 
                                    data-time="${slot.time}">
                                ${slot.display}
                            </button>
                        </div>
                    `;
                });
                slotsHtml += '</div>';
                timeSlotsContainer.innerHTML = slotsHtml;
            } else {
                timeSlotsContainer.innerHTML = '<div class="alert alert-warning">No available slots for this date.</div>';
            }
        })
        .catch(error => {
            console.error('Error loading slots:', error);
            timeSlotsContainer.innerHTML = '<div class="alert alert-danger">Error loading available slots. Please try again.</div>';
        });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading state to buttons
function addLoadingState(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="loading"></span> Loading...';
    button.disabled = true;
    
    return function() {
        button.innerHTML = originalText;
        button.disabled = false;
    };
}

// Format phone numbers
function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length >= 10) {
        value = value.substring(0, 10);
        value = value.replace(/(\d{3})(\d{3})(\d{4})/, '($1) $2-$3');
    }
    input.value = value;
}

// Add phone number formatting to phone inputs
document.querySelectorAll('input[type="tel"], input[name*="phone"]').forEach(input => {
    input.addEventListener('input', function() {
        formatPhoneNumber(this);
    });
});

// Print functionality
function printPage() {
    window.print();
}

// Export functionality (basic CSV export)
function exportToCSV(data, filename) {
    const csv = data.map(row => row.join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}