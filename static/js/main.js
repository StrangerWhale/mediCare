// Main JavaScript file for mediCare

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

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Date picker restrictions (no past dates for appointments)
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        const today = new Date().toISOString().split('T')[0];
        input.setAttribute('min', today);
    });
});

// Function to load available time slots
function loadTimeSlots(doctorId, selectedDate) {
    const slotsContainer = document.getElementById('time-slots');
    if (!slotsContainer) return;

    // Show loading
    slotsContainer.innerHTML = '<div class="text-center"><div class="loading"></div> Loading available slots...</div>';

    fetch(`/doctors/${doctorId}/slots/?date=${selectedDate}`)
        .then(response => response.json())
        .then(data => {
            if (data.slots && data.slots.length > 0) {
                let slotsHtml = '<h6>Available Time Slots:</h6><div class="d-flex flex-wrap">';
                data.slots.forEach(slot => {
                    slotsHtml += `
                        <button type="button" class="time-slot-btn" onclick="selectTimeSlot(${slot.id}, '${slot.start_time}')">
                            ${slot.start_time} - ${slot.end_time}
                        </button>
                    `;
                });
                slotsHtml += '</div>';
                slotsContainer.innerHTML = slotsHtml;
            } else {
                slotsContainer.innerHTML = '<div class="alert alert-warning">No available slots for this date.</div>';
            }
        })
        .catch(error => {
            console.error('Error loading time slots:', error);
            slotsContainer.innerHTML = '<div class="alert alert-danger">Error loading time slots. Please try again.</div>';
        });
}

// Function to select time slot
function selectTimeSlot(slotId, startTime) {
    // Remove active class from all buttons
    document.querySelectorAll('.time-slot-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Add active class to selected button
    event.target.classList.add('active');

    // Set hidden input value
    const timeSlotInput = document.getElementById('time_slot');
    if (timeSlotInput) {
        timeSlotInput.value = slotId;
    }

    // Enable submit button
    const submitBtn = document.getElementById('book-appointment-btn');
    if (submitBtn) {
        submitBtn.disabled = false;
    }
}

// Function to confirm appointment cancellation
function confirmCancellation() {
    return confirm('Are you sure you want to cancel this appointment? This action cannot be undone.');
}

// Function to format date
function formatDate(dateString) {
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        weekday: 'long'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
}

// Function to show loading state
function showLoading(element) {
    const originalContent = element.innerHTML;
    element.innerHTML = '<span class="loading"></span> Loading...';
    element.disabled = true;
    return originalContent;
}

// Function to hide loading state
function hideLoading(element, originalContent) {
    element.innerHTML = originalContent;
    element.disabled = false;
}

// Search functionality
function initializeSearch() {
    const searchInput = document.getElementById('doctor-search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const searchTerm = this.value.toLowerCase();
                const doctorCards = document.querySelectorAll('.doctor-card');
                
                doctorCards.forEach(card => {
                    const doctorName = card.querySelector('.card-title').textContent.toLowerCase();
                    const specialization = card.querySelector('.text-muted').textContent.toLowerCase();
                    
                    if (doctorName.includes(searchTerm) || specialization.includes(searchTerm)) {
                        card.style.display = 'block';
                        card.classList.add('fade-in');
                    } else {
                        card.style.display = 'none';
                    }
                });
            }, 300);
        });
    }
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeSearch);