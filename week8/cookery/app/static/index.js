document.addEventListener('DOMContentLoaded', function() {
    searchFilter()
});

function searchFilter() {
    document.addEventListener('DOMContentLoaded', function() {
        // Get the form element
        const filterForm = document.getElementById('filterForm');
        const filteredItemsContainer = document.getElementById('filteredItems');

        // Listen for changes to the checkboxes
        filterForm.addEventListener('change', async function(event) {
            // Prevent form submission if button is clicked
            if (event.target.type === 'checkbox') {
                // Send the form data using fetch
                await applyFilters();
            }
        });

        // Function to apply filters using fetch
        async function applyFilters() {
            try {
                // Create a form data object to collect the filter form's data
                const formData = new FormData(filterForm);

                // Use fetch to send the form data via GET to the server
                const response = await fetch(`${filterForm.action}`, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',  // Let server know we expect JSON
                    },
                    body: null, // No body for GET request, FormData will be appended to URL
                    // Note: `FormData` automatically appends data as query string
                    credentials: 'same-origin', // Keep session if needed (for authentication)
                });

                // Check if the response is OK
                if (response.ok) {
                    const data = await response.json(); // Parse JSON response
                    filteredItemsContainer.innerHTML = data.html; // Inject new items into the page
                } else {
                    console.error('Failed to fetch filtered data:', response.status);
                }
            } catch (error) {
                console.error('Error during fetch:', error);
            }
        }
    });
}

