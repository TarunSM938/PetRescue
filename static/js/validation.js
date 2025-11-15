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
                        .catch(() => {
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
        // Suggestions are available but not displayed in the current implementation
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
    
    // Admin Notification System
    function setupAdminNotifications() {
        // Only run for authenticated admin users
        if (!document.querySelector('.notification-badge')) {
            return;
        }
        
        let isDropdownOpen = false;
        let isLoading = false;
        let dropdownInstance = null;
        let mobileDropdownInstance = null;
        
        // Function to update notification count for both mobile and desktop
        function updateNotificationCount() {
            fetch('/api/admin/notifications/unread-count/')
                .then(response => response.json())
                .then(data => {
                    // Update desktop count
                    const countElement = document.getElementById('notification-count');
                    const totalCountElement = document.getElementById('notification-total-count');
                    
                    // Update mobile count
                    const mobileCountElement = document.getElementById('notification-count-mobile');
                    const mobileTotalCountElement = document.getElementById('notification-total-count-mobile');
                    
                    // Update desktop elements
                    if (countElement) {
                        countElement.textContent = data.unread_count;
                        countElement.style.display = data.unread_count > 0 ? 'inline' : 'none';
                        
                        // Add animation effect when new notifications arrive
                        if (data.unread_count > 0) {
                            // Remove any existing animation classes first
                            countElement.classList.remove('animate__animated', 'animate__pulse');
                            // Trigger reflow to restart animation
                            void countElement.offsetWidth;
                            // Add animation classes
                            countElement.classList.add('animate__animated', 'animate__pulse');
                            setTimeout(() => {
                                countElement.classList.remove('animate__animated', 'animate__pulse');
                            }, 1000);
                        }
                    }
                    
                    if (totalCountElement) {
                        // Will be updated when notifications are loaded
                    }
                    
                    // Update mobile elements
                    if (mobileCountElement) {
                        mobileCountElement.textContent = data.unread_count;
                        mobileCountElement.style.display = data.unread_count > 0 ? 'inline' : 'none';
                        
                        // Add animation effect when new notifications arrive
                        if (data.unread_count > 0) {
                            // Remove any existing animation classes first
                            mobileCountElement.classList.remove('animate__animated', 'animate__pulse');
                            // Trigger reflow to restart animation
                            void mobileCountElement.offsetWidth;
                            // Add animation classes
                            mobileCountElement.classList.add('animate__animated', 'animate__pulse');
                            setTimeout(() => {
                                mobileCountElement.classList.remove('animate__animated', 'animate__pulse');
                            }, 1000);
                        }
                    }
                    
                    if (mobileTotalCountElement) {
                        // Will be updated when notifications are loaded
                    }
                })
                .catch(() => {
                    // Silently handle notification count fetch errors
                });
        }
        
        // Function to create notification element HTML
        function createNotificationElementHTML(notification) {
                                // Format the timestamp
                                const timestamp = new Date(notification.timestamp);
                                const now = new Date();
                                const diffMs = now - timestamp;
                                const diffMins = Math.floor(diffMs / 60000);
                                const diffHours = Math.floor(diffMs / 3600000);
                                const diffDays = Math.floor(diffMs / 86400000);
                                
                                let timeAgo;
                                if (diffMins < 1) {
                                    timeAgo = 'Just now';
                                } else if (diffMins < 60) {
                                    timeAgo = `${diffMins}m`;
                                } else if (diffHours < 24) {
                                    timeAgo = `${diffHours}h`;
                                } else if (diffDays < 7) {
                                    timeAgo = `${diffDays}d`;
                                } else {
                                    timeAgo = timestamp.toLocaleDateString([], {month: 'short', day: 'numeric'});
                                }
                                
                                // Get notification type class
                                const typeClass = notification.notification_type === 'lost_report' ? 'lost' : 'found';
                                const typeText = notification.notification_type === 'lost_report' ? 'Lost' : 'Found';
                                
            return `
                                    <div class="notification-content">
                                        <div class="d-flex align-items-center">
                                            <div class="notification-message">${notification.message}</div>
                                            <span class="notification-type ${typeClass}">${typeText}</span>
                                        </div>
                                        <div class="notification-time">
                                            <i class="fas fa-clock"></i>
                                            ${timeAgo}
                                        </div>
                                    </div>
                                    <div class="notification-actions">
                                        <button class="btn mark-read-btn" 
                                                data-notification-id="${notification.id}"
                                                title="${notification.is_read ? 'Mark as unread' : 'Mark as read'}">
                                            <i class="fas ${notification.is_read ? 'fa-envelope' : 'fa-envelope-open'}"></i>
                                        </button>
                                        <button class="btn open-btn" 
                                                data-request-id="${notification.request.id}"
                                                title="Open report">
                                            <i class="fas fa-external-link-alt"></i>
                                        </button>
                                    </div>
                                `;
        }
                                
        // Function to attach event listeners to notification element
        function attachNotificationListeners(notificationElement, notification) {
                                // Add click event to mark as read
                                const markReadBtn = notificationElement.querySelector('.mark-read-btn');
            if (markReadBtn) {
                                markReadBtn.addEventListener('click', function(e) {
                                    e.stopPropagation();
                                    const notificationId = this.getAttribute('data-notification-id');
                                    markNotificationAsRead(notificationId, notificationElement);
                                });
            }
                                
                                // Add click event to open button
                                const openBtn = notificationElement.querySelector('.open-btn');
            if (openBtn) {
                                openBtn.addEventListener('click', function(e) {
                                    e.stopPropagation();
                                    const requestId = this.getAttribute('data-request-id');
                                    window.location.href = `/dashboard/admin/pending-requests/`;
                                });
            }
                                
                                // Add click event to the notification item
                                notificationElement.addEventListener('click', function() {
                const markBtn = this.querySelector('.mark-read-btn');
                if (markBtn) {
                    const notificationId = markBtn.getAttribute('data-notification-id');
                                    markNotificationAsRead(notificationId, this);
                                    window.location.href = `/dashboard/admin/pending-requests/`;
                }
                                });
                                
                                // Add keyboard support
                                notificationElement.addEventListener('keydown', function(e) {
                                    if (e.key === 'Enter' || e.key === ' ') {
                                        e.preventDefault();
                    const markBtn = this.querySelector('.mark-read-btn');
                    if (markBtn) {
                        const notificationId = markBtn.getAttribute('data-notification-id');
                                        markNotificationAsRead(notificationId, this);
                                        window.location.href = `/dashboard/admin/pending-requests/`;
                    }
                }
            });
        }
        
        // Function to populate a notification container with data
        function populateNotificationContainer(containerId, totalCountId, notificationsData) {
            const notificationList = document.getElementById(containerId);
            const totalCountElement = document.getElementById(totalCountId);
            
            if (!notificationList) return;
            
            notificationList.innerHTML = '';
            
            if (totalCountElement) {
                totalCountElement.textContent = notificationsData.notifications ? notificationsData.notifications.length : 0;
            }
            
            if (notificationsData.notifications && notificationsData.notifications.length > 0) {
                // Show newest notifications first (limit to 4 for home page)
                const notificationsToShow = notificationsData.notifications.slice(0, 4);
                notificationsToShow.forEach((notification) => {
                    const notificationElement = document.createElement('div');
                    notificationElement.className = `notification-item ${notification.is_read ? 'read' : 'unread'}`;
                    notificationElement.setAttribute('role', 'menuitem');
                    notificationElement.setAttribute('tabindex', '-1');
                    
                    notificationElement.innerHTML = createNotificationElementHTML(notification);
                    notificationList.appendChild(notificationElement);
                    
                    // Attach event listeners
                    attachNotificationListeners(notificationElement, notification);
                            });
                        } else {
                            const emptyElement = document.createElement('div');
                            emptyElement.className = 'notification-empty';
                            emptyElement.innerHTML = `
                                <i class="fas fa-bell-slash"></i>
                                <div>No notifications</div>
                                <small class="text-muted">You're all caught up!</small>
                            `;
                            notificationList.appendChild(emptyElement);
                        }
                    }
        
        // Function to load notifications dropdown (loads both mobile and desktop)
        function loadNotifications() {
            if (isLoading) return;
            isLoading = true;
            
            fetch('/api/admin/notifications/')
                .then(response => response.json())
                .then(data => {
                    // Populate both desktop and mobile containers with the same data
                    populateNotificationContainer('notification-list', 'notification-total-count', data);
                    populateNotificationContainer('notification-list-mobile', 'notification-total-count-mobile', data);
                    isLoading = false;
                })
                .catch(() => {
                    isLoading = false;
                });
        }
        
        // Function to mark a notification as read
        function markNotificationAsRead(notificationId, element) {
            fetch(`/api/admin/notifications/mark-read/${notificationId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update UI
                if (element) {
                    element.classList.remove('unread');
                    element.classList.add('read');
                    
                    // Update mark button icon
                    const markBtn = element.querySelector('.mark-read-btn');
                    markBtn.innerHTML = '<i class="fas fa-envelope"></i>';
                    markBtn.title = 'Mark as unread';
                }
                
                updateNotificationCount();
            })
            .catch(() => {
                // Silently handle notification mark as read errors
            });
        }
        
        // Function to mark all notifications as read
        function markAllNotificationsAsRead() {
            fetch('/api/admin/notifications/mark-all-read/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                // Update UI with animation
                const notificationItems = document.querySelectorAll('.notification-item.unread');
                notificationItems.forEach(item => {
                    item.classList.remove('unread');
                    item.classList.add('read');
                    
                    // Update mark button icon
                    const markBtn = item.querySelector('.mark-read-btn');
                    markBtn.innerHTML = '<i class="fas fa-envelope"></i>';
                    markBtn.title = 'Mark as unread';
                });
                
                updateNotificationCount();
            })
            .catch(() => {
                // Silently handle mark all notifications as read errors
            });
        }
        
        // Helper function to get CSRF token
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        
        // Function to check if dropdown is actually open (checks both desktop and mobile)
        function isDropdownActuallyOpen() {
            const desktopMenu = document.getElementById('notification-dropdown-menu');
            const mobileMenu = document.getElementById('notification-dropdown-menu-mobile');
            return (desktopMenu && desktopMenu.classList.contains('show')) || 
                   (mobileMenu && mobileMenu.classList.contains('show'));
        }
        
        // Function to close all dropdowns
        function closeAllDropdowns() {
            if (dropdownInstance) {
                dropdownInstance.hide();
            }
            if (mobileDropdownInstance) {
                mobileDropdownInstance.hide();
            }
            isDropdownOpen = false;
        }
        
        // Legacy function for backwards compatibility
        function closeDropdown() {
            closeAllDropdowns();
        }
        
        // Function to initialize a single dropdown
        function initializeDropdown(dropdownToggleId, dropdownMenuId, instanceVar) {
            const dropdownToggle = document.getElementById(dropdownToggleId);
            const dropdownMenu = document.getElementById(dropdownMenuId);
            
            if (!dropdownToggle || !dropdownMenu) {
                return null;
            }
            
            // Ensure dropdown is closed on page load - remove any show classes
                        dropdownMenu.classList.remove('show');
                        dropdownToggle.classList.remove('show');
                        dropdownToggle.setAttribute('aria-expanded', 'false');
            
            // Initialize Bootstrap dropdown with click trigger only (no hover/focus)
            let instance = null;
            try {
                instance = new bootstrap.Dropdown(dropdownToggle, {
                    trigger: 'click', // Only open on click, not hover or focus
                    boundary: 'viewport', // Keep dropdown within viewport
                    popperConfig: {
                        modifiers: [
                            {
                                name: 'preventOverflow',
                                options: {
                                    boundary: dropdownToggle.closest('.navbar') || document.body
                                }
                            }
                        ]
                    }
                });
            } catch (e) {
                // If dropdown already initialized, get existing instance
                instance = bootstrap.Dropdown.getInstance(dropdownToggle);
                if (!instance) {
                    // Fallback: create new instance with click-only trigger
                    instance = new bootstrap.Dropdown(dropdownToggle, {
                        trigger: 'click'
                    });
                }
            }
            
            // Manual click handler to toggle dropdown (since we removed data-bs-toggle)
            dropdownToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Toggle dropdown using Bootstrap's API
                const isOpen = dropdownMenu.classList.contains('show');
                if (isOpen) {
                    instance.hide();
                } else {
                    instance.show();
                }
            });
            
            // Track dropdown state using Bootstrap events
            dropdownToggle.addEventListener('show.bs.dropdown', function(e) {
                isDropdownOpen = true;
            });
            
            dropdownToggle.addEventListener('shown.bs.dropdown', function(e) {
                // Load notifications only when dropdown is actually shown
                isDropdownOpen = true;
                loadNotifications();
            });
            
            dropdownToggle.addEventListener('hide.bs.dropdown', function(e) {
                isDropdownOpen = false;
            });
            
            dropdownToggle.addEventListener('hidden.bs.dropdown', function(e) {
                // Ensure dropdown is fully closed
                isDropdownOpen = false;
                dropdownMenu.classList.remove('show');
                dropdownToggle.setAttribute('aria-expanded', 'false');
            });
            
            // Prevent dropdown from opening on non-left mouse button clicks
            dropdownToggle.addEventListener('mousedown', function(e) {
                // Only allow left mouse button clicks (button 0)
                if (e.button !== 0) {
                    e.preventDefault();
                    e.stopPropagation();
                    // Close dropdown if it's open
                    if (dropdownMenu.classList.contains('show')) {
                        instance.hide();
                    }
                }
            });
            
            return instance;
        }
        
        // Set up event listeners for desktop dropdown
        const dropdownToggle = document.getElementById('notificationDropdown');
        const markAllReadBtn = document.getElementById('mark-all-read');
        const dropdownMenu = document.getElementById('notification-dropdown-menu');
        
        // Set up event listeners for mobile dropdown
        const mobileDropdownToggle = document.getElementById('notificationDropdownMobile');
        const mobileMarkAllReadBtn = document.getElementById('mark-all-read-mobile');
        const mobileDropdownMenu = document.getElementById('notification-dropdown-menu-mobile');
        
        // Initialize desktop dropdown
        if (dropdownToggle && dropdownMenu) {
            dropdownInstance = initializeDropdown('notificationDropdown', 'notification-dropdown-menu', 'dropdownInstance');
        }
        
        // Initialize mobile dropdown
        if (mobileDropdownToggle && mobileDropdownMenu) {
            mobileDropdownInstance = initializeDropdown('notificationDropdownMobile', 'notification-dropdown-menu-mobile', 'mobileDropdownInstance');
        }
        
        // Handle Escape key to close all dropdowns
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && isDropdownActuallyOpen()) {
                e.preventDefault();
                closeAllDropdowns();
            }
        });
        
        // Close dropdown when clicking outside - handle both desktop and mobile
            document.addEventListener('click', function(e) {
            // Check if any dropdown is open
            const desktopOpen = dropdownMenu && dropdownMenu.classList.contains('show');
            const mobileOpen = mobileDropdownMenu && mobileDropdownMenu.classList.contains('show');
            
            if (!desktopOpen && !mobileOpen) {
                return;
            }
            
            // Check if click is outside desktop dropdown
            if (desktopOpen) {
                const clickedInsideDesktopToggle = dropdownToggle && (dropdownToggle === e.target || dropdownToggle.contains(e.target));
                const clickedInsideDesktopMenu = dropdownMenu && (dropdownMenu === e.target || dropdownMenu.contains(e.target));
                const clickedInsideDesktop = clickedInsideDesktopToggle || clickedInsideDesktopMenu;
                
                if (!clickedInsideDesktop) {
                        dropdownInstance.hide();
                }
            }
            
            // Check if click is outside mobile dropdown
            if (mobileOpen) {
                const clickedInsideMobileToggle = mobileDropdownToggle && (mobileDropdownToggle === e.target || mobileDropdownToggle.contains(e.target));
                const clickedInsideMobileMenu = mobileDropdownMenu && (mobileDropdownMenu === e.target || mobileDropdownMenu.contains(e.target));
                const clickedInsideMobile = clickedInsideMobileToggle || clickedInsideMobileMenu;
                
                if (!clickedInsideMobile) {
                    mobileDropdownInstance.hide();
                }
            }
        }, false); // Use bubbling phase - toggle handler uses stopPropagation so this won't fire for toggle clicks
        
        // Handle mark-all-read buttons for both desktop and mobile
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation(); // Prevent event from bubbling up
                markAllNotificationsAsRead();
            });
        }
        
        if (mobileMarkAllReadBtn) {
            mobileMarkAllReadBtn.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation(); // Prevent event from bubbling up
                markAllNotificationsAsRead();
            });
        }
        
        // Initial load - update count only, do not open dropdown
        updateNotificationCount();
        
        // Set up periodic refresh (every 30 seconds) - only update count, do not check for open state
        setInterval(() => {
            updateNotificationCount();
            // Only reload notifications if dropdown is actually open and visible
            if (isDropdownActuallyOpen() && isDropdownOpen) {
                loadNotifications();
            }
        }, 30000);
    }
    
    // Initialize admin notifications after DOM is ready
    setupAdminNotifications();
});