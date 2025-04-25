document.addEventListener('DOMContentLoaded', function() {
    // Currency formatting
    function formatCurrency(amount) {
        return 'Ksh ' + new Intl.NumberFormat('en-KE', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    // Progress calculation and display
    function updateGoalProgress(goalCard) {
        const currentSavings = parseFloat(goalCard.dataset.current);
        const targetAmount = parseFloat(goalCard.dataset.target);
        const progress = (currentSavings / targetAmount) * 100;
        
        const progressBar = goalCard.querySelector('.progress-fill');
        const progressText = goalCard.querySelector('.progress-percentage');
        
        // Update width and text
        progressBar.style.width = `${progress}%`;
        progressText.textContent = `${progress.toFixed(1)}%`;
        
        // Update color classes
        progressBar.classList.remove('completed', 'warning', 'danger');
        if (progress >= 100) {
            progressBar.classList.add('completed');
        } else if (progress >= 75) {
            progressBar.classList.add('warning');
        } else if (progress <= 25) {
            progressBar.classList.add('danger');
        }
    }

    // Initialize progress bars
    document.querySelectorAll('.goal-card').forEach(updateGoalProgress);

    // Form validation
    function validateForm(form) {
        const targetAmount = parseFloat(form.querySelector('[name="target_amount"]')?.value);
        const currentSavings = parseFloat(form.querySelector('[name="current_savings"]')?.value) || 0;
        const deadline = new Date(form.querySelector('[name="deadline"]')?.value);
        const today = new Date();

        if (targetAmount <= 0) {
            showAlert('Target amount must be greater than zero.', 'error');
            return false;
        }

        if (currentSavings > targetAmount) {
            showAlert('Current savings cannot exceed target amount.', 'error');
            return false;
        }

        if (deadline < today) {
            showAlert('Deadline must be in the future.', 'error');
            return false;
        }

        return true;
    }

    // Handle contribution modal
    const addContributionButtons = document.querySelectorAll('.add-contribution');
    const contributionModal = document.getElementById('add-contribution-modal');
    const contributionForm = document.getElementById('contribution-form');
    const amountInput = document.getElementById('amount');
    const walletBalance = parseFloat(document.querySelector('.wallet-balance')?.textContent.replace(/[^0-9.-]+/g, '') || '0');

    addContributionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const goalId = this.dataset.id;
            const goalName = this.dataset.name;
            
            document.getElementById('goal-id').value = goalId;
            document.querySelector('#add-contribution-modal .modal-title').textContent = 
                `Add Contribution to ${goalName}`;
            
            // Reset form
            contributionForm.reset();
            amountInput.max = walletBalance;
            
            const modal = new bootstrap.Modal(contributionModal);
            modal.show();
        });
    });

    // Validate contribution amount against wallet balance
    amountInput?.addEventListener('input', function() {
        const amount = parseFloat(this.value);
        if (amount > walletBalance) {
            this.setCustomValidity('Amount cannot exceed your wallet balance');
        } else if (amount <= 0) {
            this.setCustomValidity('Amount must be greater than zero');
        } else {
            this.setCustomValidity('');
        }
    });

    // Handle contribution form submission
    contributionForm?.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const amount = parseFloat(amountInput.value);
        if (amount > walletBalance) {
            showAlert('Contribution amount cannot exceed your wallet balance', 'error');
            return;
        }

        const formData = new FormData(this);
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        
        fetch('/goals/add-contribution/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                showAlert('Contribution added successfully!', 'success');
                location.reload(); // Reload to update all balances
            } else {
                showAlert(data.message || 'Error adding contribution', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('Error adding contribution', 'error');
        })
        .finally(() => {
            submitButton.disabled = false;
        });
    });

    // Goal form handling
    document.querySelectorAll('.goal-form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });

    // Edit goal handling
    document.querySelectorAll('.edit-goal').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const goalId = this.dataset.id;
            
            fetch(`/goals/${goalId}/edit/`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.querySelector('#edit-goal-modal .modal-body').innerHTML = html;
                const modal = new bootstrap.Modal(document.getElementById('edit-goal-modal'));
                modal.show();
            });
        });
    });

    // Delete goal handling
    document.querySelectorAll('.delete-goal').forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
            const goalId = this.dataset.id;
            const goalName = this.dataset.name;

            const result = await Swal.fire({
                title: 'Delete Goal?',
                text: `Are you sure you want to delete "${goalName}"?`,
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                confirmButtonText: 'Yes, delete it!'
            });

            if (result.isConfirmed) {
                fetch(`/goals/${goalId}/delete/`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        Swal.fire(
                            'Deleted!',
                            'Your goal has been deleted.',
                            'success'
                        ).then(() => {
                            location.reload();
                        });
                    } else {
                        Swal.fire(
                            'Error!',
                            data.message || 'Could not delete the goal.',
                            'error'
                        );
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    Swal.fire(
                        'Error!',
                        'An error occurred while deleting the goal.',
                        'error'
                    );
                });
            }
        });
    });

    // Helper function to show alerts
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const messagesContainer = document.querySelector('.messages') || document.createElement('div');
        if (!document.querySelector('.messages')) {
            messagesContainer.className = 'messages';
            document.querySelector('.page-container').prepend(messagesContainer);
        }
        
        messagesContainer.appendChild(alertDiv);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
            if (messagesContainer.children.length === 0) {
                messagesContainer.remove();
            }
        }, 5000);
    }
});