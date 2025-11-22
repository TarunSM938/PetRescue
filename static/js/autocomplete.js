/*
PetRescue Autocomplete Functionality
Provides autocomplete for breed and location inputs
*/

document.addEventListener('DOMContentLoaded', function() {
    // Get breed and location input elements
    const breedInputs = document.querySelectorAll('input[name="breed"]');
    const locationInputs = document.querySelectorAll('input[name="location"]');
    
    // Sample breed data - in a real application, this would come from the server
    const commonBreeds = [
        'Labrador Retriever', 'German Shepherd', 'Golden Retriever', 'French Bulldog',
        'Bulldog', 'Poodle', 'Beagle', 'Rottweiler', 'German Shorthaired Pointer',
        'Dachshund', 'Corgi', 'Boxer', 'Siberian Husky', 'Great Dane', 'Doberman Pinscher',
        'Shiba Inu', 'Australian Shepherd', 'Border Collie', 'Brittany', 'Cavalier King Charles Spaniel',
        'Pomeranian', 'Yorkshire Terrier', 'Shih Tzu', 'Boston Terrier', 'Miniature Schnauzer',
        'Basset Hound', 'Mastiff', 'Cocker Spaniel', 'Collie', 'Maltese',
        'Pug', 'West Highland White Terrier', 'Chihuahua', 'Vizsla', 'Soft Coated Wheaten Terrier',
        'Airedale Terrier', 'Whippet', 'Scottish Terrier', 'American Staffordshire Terrier', 'Pointer'
    ];
    
    // Sample location data - in a real application, this would come from the server
    const commonLocations = [
        'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ',
        'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA',
        'Austin, TX', 'Jacksonville, FL', 'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC',
        'San Francisco, CA', 'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC',
        'Boston, MA', 'El Paso, TX', 'Nashville, TN', 'Detroit, MI', 'Oklahoma City, OK',
        'Portland, OR', 'Las Vegas, NV', 'Memphis, TN', 'Louisville, KY', 'Baltimore, MD'
    ];
    
    // Add autocomplete to breed inputs
    breedInputs.forEach(input => {
        setupAutocomplete(input, commonBreeds);
    });
    
    // Add autocomplete to location inputs
    locationInputs.forEach(input => {
        setupAutocomplete(input, commonLocations);
    });
    
    // Setup autocomplete functionality
    function setupAutocomplete(input, dataList) {
        // Create container for suggestions
        const container = document.createElement('div');
        container.className = 'autocomplete-container';
        container.style.cssText = `
            position: absolute;
            z-index: 1000;
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            max-height: 200px;
            overflow-y: auto;
            width: 100%;
            display: none;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        `;
        
        // Insert container after input
        input.parentNode.style.position = 'relative';
        input.parentNode.insertBefore(container, input.nextSibling);
        
        // Track if suggestions are visible
        let suggestionsVisible = false;
        
        // Track selected suggestion index
        let selectedIndex = -1;
        
        // Debounce timer
        let debounceTimer;
        
        // Handle input changes
        input.addEventListener('input', function() {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                const value = this.value.trim().toLowerCase();
                
                if (value.length < 2) {
                    hideSuggestions();
                    return;
                }
                
                // Filter suggestions
                const suggestions = dataList.filter(item => 
                    item.toLowerCase().includes(value)
                ).slice(0, 8); // Limit to 8 suggestions
                
                if (suggestions.length > 0) {
                    showSuggestions(suggestions);
                } else {
                    hideSuggestions();
                }
            }, 300); // 300ms debounce
        });
        
        // Handle focus
        input.addEventListener('focus', function() {
            const value = this.value.trim().toLowerCase();
            
            if (value.length >= 2) {
                const suggestions = dataList.filter(item => 
                    item.toLowerCase().includes(value)
                ).slice(0, 8);
                
                if (suggestions.length > 0) {
                    showSuggestions(suggestions);
                }
            }
        });
        
        // Handle blur (with slight delay to allow clicks on suggestions)
        input.addEventListener('blur', function() {
            setTimeout(hideSuggestions, 150);
        });
        
        // Handle keyboard navigation
        input.addEventListener('keydown', function(e) {
            if (!suggestionsVisible) return;
            
            const items = container.querySelectorAll('.autocomplete-item');
            
            switch(e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
                    updateSelection(items);
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    selectedIndex = Math.max(selectedIndex - 1, -1);
                    updateSelection(items);
                    break;
                    
                case 'Enter':
                    e.preventDefault();
                    if (selectedIndex >= 0 && selectedIndex < items.length) {
                        selectSuggestion(items[selectedIndex].textContent);
                    }
                    break;
                    
                case 'Escape':
                    hideSuggestions();
                    break;
            }
        });
        
        // Show suggestions
        function showSuggestions(suggestions) {
            container.innerHTML = '';
            selectedIndex = -1;
            
            suggestions.forEach((suggestion, index) => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.textContent = suggestion;
                item.style.cssText = `
                    padding: 8px 12px;
                    cursor: pointer;
                    border-bottom: 1px solid #eee;
                `;
                
                item.addEventListener('mouseenter', () => {
                    selectedIndex = index;
                    updateSelection(container.querySelectorAll('.autocomplete-item'));
                });
                
                item.addEventListener('click', () => {
                    selectSuggestion(suggestion);
                });
                
                container.appendChild(item);
            });
            
            container.style.display = 'block';
            suggestionsVisible = true;
            
            // Position container below input
            const rect = input.getBoundingClientRect();
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            container.style.top = (rect.bottom + scrollTop) + 'px';
            container.style.left = (rect.left + window.pageXOffset) + 'px';
            container.style.width = rect.width + 'px';
        }
        
        // Hide suggestions
        function hideSuggestions() {
            container.style.display = 'none';
            suggestionsVisible = false;
            selectedIndex = -1;
        }
        
        // Update selection highlighting
        function updateSelection(items) {
            items.forEach((item, index) => {
                if (index === selectedIndex) {
                    item.style.backgroundColor = '#f0f0f0';
                } else {
                    item.style.backgroundColor = '';
                }
            });
        }
        
        // Select a suggestion
        function selectSuggestion(value) {
            input.value = value;
            hideSuggestions();
            input.focus();
            
            // Dispatch input event to trigger any attached listeners
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
        
        // Handle window resize to reposition container
        window.addEventListener('resize', () => {
            if (suggestionsVisible) {
                const rect = input.getBoundingClientRect();
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                container.style.top = (rect.bottom + scrollTop) + 'px';
                container.style.left = (rect.left + window.pageXOffset) + 'px';
                container.style.width = rect.width + 'px';
            }
        });
    }
});