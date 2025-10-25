/*
PetRescue Form Validation and UI Enhancements
Client-side validation for registration and login forms with UI enhancements
*/

document.addEventListener('DOMContentLoaded', function() {
    // Get form elements
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    
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
            if (link.textContent === 'Report Lost Pet' && currentPage === '/adopt/' && petType === 'lost') {
                link.classList.add('active');
            } else if (link.textContent === 'Report Found Pet' && currentPage === '/adopt/' && petType === 'found') {
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