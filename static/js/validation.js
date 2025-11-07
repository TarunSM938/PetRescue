/*
PetRescue Form Validation and UI Enhancements
Client-side validation for registration and login forms with UI enhancements
*/

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const searchForm = document.getElementById('pet-search-form');
    
    // Add event listeners if forms exist
    if (registerForm) {
        registerForm.addEventListener('submit', validateRegistration);
        setupRealTimeValidation();
    }
    
    if (loginForm) {
        loginForm.addEventListener('submit', validateLogin);
    }
    
    // Add focus to first input field when modal is shown
    const logoutModal = document.getElementById('logoutModal');
    if (logoutModal) {
        logoutModal.addEventListener('shown.bs.modal', function () {
            // Add any focus or animation effects here if needed
        });
    }
    
    // Add scroll animation to elements
    setupScrollAnimations();
    
    // Add hover effects to buttons
    setupButtonHoverEffects();
    
    // Set active nav link
    setActiveNavLink();
    
    // Setup search form enhancements if it exists
    if (searchForm) {
        setupSearchFormEnhancements();
    }
    
    // Setup contact reporter functionality
    setupContactReporter();
    
    // Real-time validation setup
    function setupRealTimeValidation() {
        const emailField = document.getElementById('id_email');
        const password1Field = document.getElementById('id_password1');
        const password2Field = document.getElementById('id_password2');
        const fullNameField = document.getElementById('id_full_name');
        const phoneField = document.getElementById('id_phone');
        const usernameField = document.getElementById('id_username');
        
        if (emailField) {
            emailField.addEventListener('blur', validateEmailFormat);
            emailField.addEventListener('input', clearEmailStatus);
        }
        
        if (password1Field) {
            password1Field.addEventListener('blur', validatePasswordStrength);
            password1Field.addEventListener('input', clearPasswordHelp);
        }
        
        if (password2Field) {
            password2Field.addEventListener('input', validatePasswordMatch);
        }
        
        if (fullNameField) {
            fullNameField.addEventListener('blur', validateFullName);
        }
        
        if (phoneField) {
            phoneField.addEventListener('blur', validatePhone);
        }
        
        if (usernameField) {
            usernameField.addEventListener('blur', validateUsername);
        }
    }
    
    // Setup search form enhancements
    function setupSearchFormEnhancements() {
        // Get search form elements
        const breedInput = document.querySelector('[name="breed"]');
        const locationInput = document.querySelector('[name="location"]');
        const startDateInput = document.querySelector('[name="start_date"]');
        const endDateInput = document.querySelector('[name="end_date"]');
        const searchButton = document.getElementById('search-button');
        
        // Add debounced input listeners for text fields
        if (breedInput) {
            let breedTimeout;
            breedInput.addEventListener('input', function() {
                clearTimeout(breedTimeout);
                breedTimeout = setTimeout(() => {
                    // Could implement auto-search here if needed
                    // For now, we'll just show suggestions
                    suggestBreedCorrections(breedInput.value);
                }, 500); // 500ms debounce
            });
        }
        
        if (locationInput) {
            let locationTimeout;
            locationInput.addEventListener('input', function() {
                clearTimeout(locationTimeout);
                locationTimeout = setTimeout(() => {
                    // Could implement auto-search here if needed
                }, 500); // 500ms debounce
            });
        }
        
        // Add date validation
        if (startDateInput && endDateInput) {
            startDateInput.addEventListener('change', validateDateRange);
            endDateInput.addEventListener('change', validateDateRange);
        }
        
        // Add form submission handler
        searchForm.addEventListener('submit', function(e) {
            // Validate date range
            if (!validateDateRange()) {
                e.preventDefault();
                return false;
            }
            
            // Show loading state
            if (searchButton) {
                const spinner = searchButton.querySelector('.spinner-border');
                const text = searchButton.querySelector('#search-text');
                if (spinner && text) {
                    spinner.classList.remove('d-none');
                    text.textContent = 'Searching...';
                    searchButton.disabled = true;
                }
            }
        });
    }
    
    // Setup contact reporter functionality
    function setupContactReporter() {
        // Handle copy contact buttons
        const copyContactButtons = document.querySelectorAll('.copy-contact-btn');
        copyContactButtons.forEach(button => {
            button.addEventListener('click', function() {
                const contactType = this.getAttribute('data-contact-type');
                let contactInfo = '';
                
                if (contactType === 'phone') {
                    const phoneElement = document.getElementById('reporter-phone');
                    if (phoneElement) {
                        contactInfo = phoneElement.textContent;
                    }
                } else if (contactType === 'email') {
                    const emailElement = document.getElementById('reporter-email');
                    if (emailElement) {
                        contactInfo = emailElement.textContent;
                    }
                }
                
                // Copy to clipboard
                if (contactInfo && contactInfo !== 'Phone number not available' && contactInfo !== 'Email not available') {
                    copyToClipboard(contactInfo)
                        .then(() => {
                            // Show success feedback
                            const originalText = this.innerHTML;
                            this.innerHTML = '<i class="fas fa-check me-1"></i> Copied!';
                            setTimeout(() => {
                                this.innerHTML = originalText;
                            }, 2000);
                        })
                        .catch(err => {
                            console.error('Failed to copy: ', err);
                            alert(`Copy ${contactType} to clipboard: ${contactInfo}`);
                        });
                } else {
                    alert('Contact information is not available. Please sign in to view contact details.');
                }
            });
        });
        
        // Handle phone number click for mobile
        const phoneElements = document.querySelectorAll('#reporter-phone');
        phoneElements.forEach(element => {
            element.addEventListener('click', function() {
                const phoneText = this.textContent.trim();
                if (phoneText && phoneText !== 'Phone number not available') {
                    // On mobile, this will initiate a call
                    window.location.href = `tel:${phoneText}`;
                }
            });
        });
    }
    
    // Copy text to clipboard
    function copyToClipboard(text) {
        if (navigator.clipboard && window.isSecureContext) {
            // Use Clipboard API if available
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            textArea.style.top = '-999999px';
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            return new Promise((resolve, reject) => {
                document.execCommand('copy') ? resolve() : reject();
                textArea.remove();
            });
        }
    }
    
    // Simple fuzzy matching for breed suggestions
    function suggestBreedCorrections(input) {
        if (!input || input.length < 2) return;
        
        const commonBreeds = [
            'Labrador', 'German Shepherd', 'Golden Retriever', 'French Bulldog',
            'Siberian Husky', 'Poodle', 'Chihuahua', 'Boxer', 'Dachshund',
            'Beagle', 'Rottweiler', 'Pointer', 'Shiba Inu', 'Corgi'
        ];
        
        const inputLower = input.toLowerCase();
        const suggestions = commonBreeds.filter(breed => 
            breed.toLowerCase().includes(inputLower) || 
            levenshteinDistance(breed.toLowerCase(), inputLower) <= 2
        );
        
        // In a real implementation, we would show these suggestions to the user
        // For now, we'll just log them to the console
        if (suggestions.length > 0) {
            console.log('Did you mean:', suggestions[0]);
        }
    }
    
    // Simple Levenshtein distance implementation for fuzzy matching
    function levenshteinDistance(str1, str2) {
        const track = Array(str2.length + 1).fill(null).map(() => Array(str1.length + 1).fill(null));
        
        for (let i = 0; i <= str1.length; i += 1) {
            track[0][i] = i;
        }
        
        for (let j = 0; j <= str2.length; j += 1) {
            track[j][0] = j;
        }
        
        for (let j = 1; j <= str2.length; j += 1) {
            for (let i = 1; i <= str1.length; i += 1) {
                const indicator = str1[i - 1] === str2[j - 1] ? 0 : 1;
                track[j][i] = Math.min(
                    track[j][i - 1] + 1, // deletion
                    track[j - 1][i] + 1, // insertion
                    track[j - 1][i - 1] + indicator, // substitution
                );
            }
        }
        
        return track[str2.length][str1.length];
    }
    
    // Validate date range
    function validateDateRange() {
        const startDateInput = document.querySelector('[name="start_date"]');
        const endDateInput = document.querySelector('[name="end_date"]');
        const dateError = document.getElementById('date-error');
        
        if (!startDateInput || !endDateInput) return true;
        
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;
        
        // If both dates are provided, check that start is before end
        if (startDate && endDate && new Date(startDate) > new Date(endDate)) {
            if (dateError) {
                dateError.classList.remove('d-none');
            }
            return false;
        } else {
            if (dateError) {
                dateError.classList.add('d-none');
            }
            return true;
        }
    }
    
    // Validate registration form
    function validateRegistration(e) {
        const fullName = document.getElementById('id_full_name');
        const email = document.getElementById('id_email');
        const phone = document.getElementById('id_phone');
        const username = document.getElementById('id_username');
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        
        let isValid = true;
        
        // Clear previous error messages
        clearErrorMessages();
        
        // Validate full name
        if (!fullName.value.trim()) {
            showError(fullName, 'Full name is required.');
            isValid = false;
        } else if (fullName.value.trim().length < 2) {
            showError(fullName, 'Full name must be at least 2 characters.');
            isValid = false;
        }
        
        // Validate username
        if (!username.value.trim()) {
            showError(username, 'Username is required.');
            isValid = false;
        } else if (username.value.length < 3) {
            showError(username, 'Username must be at least 3 characters.');
            isValid = false;
        }
        
        // Validate email
        if (!email.value.trim()) {
            showError(email, 'Email is required.');
            isValid = false;
        } else if (!isValidEmail(email.value)) {
            showError(email, 'Please enter a valid email address.');
            isValid = false;
        }
        
        // Validate phone (optional but if provided, should be valid)
        if (phone.value && !isValidPhone(phone.value)) {
            showError(phone, 'Please enter a valid phone number.');
            isValid = false;
        }
        
        // Validate passwords
        if (!password1.value) {
            showError(password1, 'Password is required.');
            isValid = false;
        } else if (password1.value.length < 8) {
            showError(password1, 'Password must be at least 8 characters.');
            isValid = false;
        }
        
        if (password1.value !== password2.value) {
            showError(password2, 'Passwords do not match.');
            isValid = false;
        }
        
        // Prevent form submission if validation fails
        if (!isValid) {
            e.preventDefault();
            return false;
        }
        
        return true;
    }
    
    // Validate login form
    function validateLogin(e) {
        const username = document.querySelector('[name="username"]');
        const password = document.querySelector('[name="password"]');
        
        let isValid = true;
        
        // Clear previous error messages
        clearErrorMessages();
        
        // Validate username
        if (!username.value.trim()) {
            showError(username, 'Username is required.');
            isValid = false;
        }
        
        // Validate password
        if (!password.value) {
            showError(password, 'Password is required.');
            isValid = false;
        }
        
        // Prevent form submission if validation fails
        if (!isValid) {
            e.preventDefault();
            return false;
        }
        
        return true;
    }
    
    // Real-time full name validation
    function validateFullName() {
        const fullName = this;
        if (fullName.value.trim() === '') {
            return;
        }
        
        if (fullName.value.trim().length < 2) {
            showInlineMessage(fullName, 'Full name should be at least 2 characters.', 'error');
        } else {
            showInlineMessage(fullName, 'Looks good!', 'success');
        }
    }
    
    // Real-time username validation
    function validateUsername() {
        const username = this;
        if (username.value.trim() === '') {
            return;
        }
        
        if (username.value.length < 3) {
            showInlineMessage(username, 'Username should be at least 3 characters.', 'error');
        } else {
            showInlineMessage(username, 'Valid username', 'success');
        }
    }
    
    // Real-time phone validation
    function validatePhone() {
        const phone = this;
        if (phone.value.trim() === '') {
            return;
        }
        
        if (isValidPhone(phone.value)) {
            showInlineMessage(phone, 'Valid phone number', 'success');
        } else {
            showInlineMessage(phone, 'Please enter a valid phone number', 'error');
        }
    }
    
    // Real-time email validation
    function validateEmailFormat() {
        const email = this;
        const emailStatus = document.getElementById('email-status');
        
        if (email.value.trim() === '') {
            if (emailStatus) emailStatus.innerHTML = '';
            return;
        }
        
        if (isValidEmail(email.value)) {
            if (emailStatus) {
                emailStatus.innerHTML = '<span style="color: green;">Valid email format</span>';
            }
        } else {
            if (emailStatus) {
                emailStatus.innerHTML = '<span style="color: red;">Invalid email format</span>';
            }
        }
    }
    
    // Clear email status
    function clearEmailStatus() {
        const emailStatus = document.getElementById('email-status');
        if (emailStatus) emailStatus.innerHTML = '';
    }
    
    // Real-time password strength validation
    function validatePasswordStrength() {
        const password = this;
        const passwordHelp = document.getElementById('password-help');
        
        if (password.value === '') {
            if (passwordHelp) passwordHelp.innerHTML = '';
            return;
        }
        
        if (password.value.length < 8) {
            if (passwordHelp) {
                passwordHelp.innerHTML = '<span style="color: red;">At least 8 characters required</span>';
            }
        } else {
            if (passwordHelp) {
                passwordHelp.innerHTML = '<span style="color: green;">Good password length</span>';
            }
        }
    }
    
    // Clear password help
    function clearPasswordHelp() {
        const passwordHelp = document.getElementById('password-help');
        if (passwordHelp && passwordHelp.innerHTML.includes('Good password length')) {
            passwordHelp.innerHTML = '';
        }
    }
    
    // Real-time password match validation
    function validatePasswordMatch() {
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        const passwordMatch = document.getElementById('password-match');
        
        if (!password1 || !password2 || !passwordMatch) return;
        
        if (password2.value === '') {
            passwordMatch.innerHTML = '';
            return;
        }
        
        if (password1.value === password2.value) {
            passwordMatch.innerHTML = '<span style="color: green;">Passwords match</span>';
        } else {
            passwordMatch.innerHTML = '<span style="color: red;">Passwords do not match</span>';
        }
    }
    
    // Email format validation helper
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Phone validation helper
    function isValidPhone(phone) {
        // Allow common phone formats
        const phoneRegex = /^[0-9+\-\s()]{10,15}$/;
        return phoneRegex.test(phone);
    }
    
    // Show inline message
    function showInlineMessage(field, message, type) {
        // Remove any existing message for this field
        const existingMessage = field.parentNode.querySelector('.inline-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `inline-message mt-1 small ${type === 'error' ? 'text-danger' : 'text-success'}`;
        messageDiv.textContent = message;
        
        // Insert message after the field
        field.parentNode.insertBefore(messageDiv, field.nextSibling);
    }
    
    // Show error message
    function showError(field, message) {
        // Remove any existing error for this field
        const existingError = field.parentNode.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }
        
        // Create error message element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'text-danger error-message small mt-1';
        errorDiv.textContent = message;
        
        // Insert error after the field
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    // Clear all error messages
    function clearErrorMessages() {
        const errorMessages = document.querySelectorAll('.error-message, .inline-message');
        errorMessages.forEach(error => error.remove());
    }
    
    // Set up scroll animations
    function setupScrollAnimations() {
        // Add fade-in animation to elements when they come into view
        const fadeElements = document.querySelectorAll('.feature-card, .pet-card, .cta-section .card');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, {
            threshold: 0.1
        });
        
        fadeElements.forEach(element => {
            observer.observe(element);
        });
    }
    
    // Set up button hover effects
    function setupButtonHoverEffects() {
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            button.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    }
    
    // Set active nav link based on current page
    function setActiveNavLink() {
        const links = document.querySelectorAll('.nav-link');
        const currentPage = window.location.pathname;
        const urlParams = new URLSearchParams(window.location.search);
        const petType = urlParams.get('type');
        
        links.forEach(link => {
            // Remove active class from all links
            link.classList.remove('active');
            
            // Add active class to current page link
            const linkHref = link.getAttribute('href');
            
            // Special handling for Report Lost Pet and Report Found Pet links
            if (link.textContent === 'Report Lost Pet' && currentPage === '/find-pets/' && petType === 'lost') {
                link.classList.add('active');
            } else if (link.textContent === 'Report Found Pet' && currentPage === '/find-pets/' && petType === 'found') {
                link.classList.add('active');
            } else if (linkHref === currentPage) {
                link.classList.add('active');
            }
            
            // Special case for home page
            if (currentPage === '/' && linkHref === '/') {
                link.classList.add('active');
            }
        });
    }
});