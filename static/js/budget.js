document.addEventListener('DOMContentLoaded', function() {
    // Currency formatting
    function formatCurrency(amount) {
        return 'Ksh ' + new Intl.NumberFormat('en-KE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    // Format currency inputs on blur
    document.querySelectorAll('input[type="number"]').forEach(input => {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });

    // Real-time budget percentage calculation
    const limitInput = document.getElementById('id_limit');
    const amountSpentInput = document.getElementById('id_amount_spent');
    const percentageDisplay = document.querySelector('.progress-text');
    const progressBar = document.querySelector('.progress-bar');

    function updatePercentage() {
        if (limitInput && amountSpentInput && percentageDisplay && progressBar) {
            const limit = parseFloat(limitInput.value) || 0;
            const spent = parseFloat(amountSpentInput.value) || 0;
            
            if (limit > 0) {
                const percentage = (spent / limit) * 100;
                percentageDisplay.textContent = percentage.toFixed(1) + '% used';
                progressBar.style.width = percentage + '%';
                
                // Update progress bar color
                if (percentage >= 90) {
                    progressBar.className = 'progress-bar danger';
                } else if (percentage >= 75) {
                    progressBar.className = 'progress-bar warning';
                } else {
                    progressBar.className = 'progress-bar';
                }
            }
        }
    }

    if (limitInput && amountSpentInput) {
        limitInput.addEventListener('input', updatePercentage);
        amountSpentInput.addEventListener('input', updatePercentage);
    }

    // Form validation
    document.querySelectorAll('.budget-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const limit = parseFloat(this.querySelector('#id_limit').value) || 0;
            const amountSpent = parseFloat(this.querySelector('#id_amount_spent').value) || 0;

            if (limit <= 0) {
                e.preventDefault();
                alert('Monthly limit must be greater than zero.');
                return false;
            }

            if (amountSpent > limit) {
                e.preventDefault();
                alert('Amount spent cannot exceed the monthly limit.');
                return false;
            }
        });
    });

    // Delete confirmation with SweetAlert if available
    document.querySelectorAll('.delete-budget').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const budgetId = this.dataset.id;

            if (window.Swal) {
                Swal.fire({
                    title: 'Delete Budget?',
                    text: 'This action cannot be undone.',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#dc3545',
                    cancelButtonColor: '#6c757d',
                    confirmButtonText: 'Yes, delete it!'
                }).then((result) => {
                    if (result.isConfirmed) {
                        deleteBudget(budgetId);
                    }
                });
            } else {
                if (confirm('Are you sure you want to delete this budget? This action cannot be undone.')) {
                    deleteBudget(budgetId);
                }
            }
        });
    });

    function deleteBudget(budgetId) {
        fetch(`/budget/${budgetId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        }).then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Error deleting budget. Please try again.');
            }
        });
    }

    // Filter functionality
    const filterForm = document.getElementById('filters-form');
    const startDateInput = filterForm?.querySelector('input[name="start_date"]');
    const endDateInput = filterForm?.querySelector('input[name="end_date"]');
    const categoryFilter = document.getElementById('category-filter');

    if (startDateInput && endDateInput) {
        // Validate date range
        startDateInput.addEventListener('change', function() {
            endDateInput.min = this.value;
            validateDates();
        });

        endDateInput.addEventListener('change', function() {
            startDateInput.max = this.value;
            validateDates();
        });

        function validateDates() {
            const startDate = new Date(startDateInput.value);
            const endDate = new Date(endDateInput.value);
            const submitBtn = filterForm.querySelector('button[type="submit"]');

            if (startDate > endDate) {
                submitBtn.disabled = true;
                showAlert('End date must be after start date', 'warning');
            } else {
                submitBtn.disabled = false;
            }
        }
    }

    // Category quick filter
    if (categoryFilter) {
        categoryFilter.addEventListener('change', function() {
            filterForm.submit();
        });
    }

    // Show alert function using SweetAlert if available
    function showAlert(message, type = 'info') {
        if (window.Swal) {
            Swal.fire({
                text: message,
                icon: type,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000
            });
        } else {
            alert(message);
        }
    }

    // Clear filters
    const clearFiltersBtn = document.querySelector('a[href*="budget:budgets"]');
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function(e) {
            e.preventDefault();
            // Clear all form inputs
            filterForm.reset();
            // Submit the form to refresh the page without filters
            filterForm.submit();
        });
    }

    // Format currency values
    document.querySelectorAll('.budget-amount .value').forEach(element => {
        const value = element.textContent.trim().replace('KES', '').trim();
        element.textContent = formatCurrency(value);
    });

    // Format currency function
    function formatCurrency(amount) {
        return 'Ksh ' + new Intl.NumberFormat('en-KE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }
});