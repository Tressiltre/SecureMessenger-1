// CryptoSecure App - Main JavaScript file

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize file upload handlers
    initializeFileUploads();
    
    // Initialize form validations
    initializeFormValidations();
    
    // Initialize copy to clipboard functionality
    initializeCopyButtons();
    
    // Initialize character counters
    initializeCharacterCounters();
}

// File upload handling
function initializeFileUploads() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                validateFileUpload(file, input);
            }
        });
    });
}

function validateFileUpload(file, input) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp'];
    
    // Check file size
    if (file.size > maxSize) {
        showAlert('File size too large. Maximum size is 16MB.', 'danger');
        input.value = '';
        return false;
    }
    
    // Check file type
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or BMP files.', 'danger');
        input.value = '';
        return false;
    }
    
    // Show file info
    const fileName = file.name;
    const fileSize = formatFileSize(file.size);
    showAlert(`File selected: ${fileName} (${fileSize})`, 'info');
    
    return true;
}

// Form validation
function initializeFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form)) {
                e.preventDefault();
                e.stopPropagation();
            } else {
                // Show loading state
                showLoadingState(form);
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'This field is required.');
            isValid = false;
        } else {
            clearFieldError(input);
        }
    });
    
    // Special validations
    const passwordField = form.querySelector('input[name="password"]');
    const confirmPasswordField = form.querySelector('input[name="confirm_password"]');
    
    if (passwordField && confirmPasswordField) {
        if (passwordField.value !== confirmPasswordField.value) {
            showFieldError(confirmPasswordField, 'Passwords do not match.');
            isValid = false;
        }
        
        if (passwordField.value.length < 6) {
            showFieldError(passwordField, 'Password must be at least 6 characters long.');
            isValid = false;
        }
    }
    
    // Message length validation for encryption
    const messageField = form.querySelector('textarea[name="message"]');
    if (messageField && form.action.includes('encrypt')) {
        if (messageField.value.length > 190) {
            showFieldError(messageField, 'Message too long for RSA encryption (max 190 characters).');
            isValid = false;
        }
    }
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function clearFieldError(field) {
    field.classList.remove('is-invalid');
    const errorDiv = field.parentNode.querySelector('.invalid-feedback');
    if (errorDiv) {
        errorDiv.remove();
    }
}

// Copy to clipboard functionality
function initializeCopyButtons() {
    // This function is called from templates, so it's available globally
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copied to clipboard!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showAlert('Copied to clipboard!', 'success');
    } catch (err) {
        showAlert('Failed to copy to clipboard. Please copy manually.', 'warning');
    }
    
    document.body.removeChild(textArea);
}

// Character counters
function initializeCharacterCounters() {
    const textareas = document.querySelectorAll('textarea');
    
    textareas.forEach(textarea => {
        if (textarea.name === 'message' && window.location.pathname.includes('encrypt')) {
            addCharacterCounter(textarea, 190);
        }
    });
}

function addCharacterCounter(element, maxLength) {
    const counter = document.createElement('div');
    counter.className = 'form-text character-counter';
    counter.style.textAlign = 'right';
    element.parentNode.appendChild(counter);
    
    function updateCounter() {
        const remaining = maxLength - element.value.length;
        counter.textContent = `${element.value.length}/${maxLength} characters`;
        
        if (remaining < 20) {
            counter.className = 'form-text character-counter text-warning';
        } else if (remaining < 0) {
            counter.className = 'form-text character-counter text-danger';
        } else {
            counter.className = 'form-text character-counter';
        }
    }
    
    element.addEventListener('input', updateCounter);
    updateCounter();
}

// Alert system
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Loading states
function showLoadingState(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    if (submitButton) {
        submitButton.disabled = true;
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2" role="status"></span>
            Processing...
        `;
        
        // Store original text for restoration if needed
        submitButton.dataset.originalText = originalText;
    }
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Password strength indicator
function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    const levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['danger', 'warning', 'info', 'success', 'success'];
    
    return {
        level: levels[strength],
        color: colors[strength],
        score: strength
    };
}

// Initialize password strength indicator if password field exists
document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.querySelector('input[name="password"]');
    if (passwordField && passwordField.form.action.includes('register')) {
        const strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength mt-1';
        passwordField.parentNode.appendChild(strengthIndicator);
        
        passwordField.addEventListener('input', function() {
            const strength = checkPasswordStrength(this.value);
            strengthIndicator.innerHTML = `
                <small class="text-${strength.color}">
                    Password strength: ${strength.level}
                </small>
            `;
        });
    }
});

// Export functions for global use
window.copyToClipboard = copyToClipboard;
window.showAlert = showAlert;
