document.addEventListener('DOMContentLoaded', function() {
    starRating();
    fadeMessage();
    averageRating();
    initEditButton();
});

// Function to colour rating stars when clicked
function starRating() {
    const stars = document.querySelectorAll(".star-rating-input");
    const labels = document.querySelectorAll(".star-rating-label");

    // Click event: Mark stars gold up to the clicked star
    stars.forEach((star, index) => {
        star.addEventListener("click", function() {
            // Color the stars gold up to and including the clicked one
            for (let i = 0; i <= index; i++) {
                labels[i].style.color = "gold"; 
            }

            // Reset the colors for the rest of the stars
            for (let i = index + 1; i < stars.length; i++) {
                labels[i].style.color = "#ccc"; // Reset the rest to the default color
            }
        });
    });
}

// Function to fade Django messages - ex. after rating recipe
function fadeMessage() {
    // Select the first alert and star-rating container
    var message = document.querySelector(".alert");
    const starRatingContainer = document.querySelector(".star-rating-container");

    // Ensure both elements are found
    if (message && starRatingContainer) {
        // Add 'hide' class to the message after 3 seconds
        setTimeout(function() {
            message.classList.add("hide");

            // Add 'move-up' class to the star rating container after the message fades
            setTimeout(function() {
                starRatingContainer.classList.add("move-up");
            }, 250); // Match the fade duration of the alert (250ms delay)

        }, 3000); // Wait 3 seconds before hiding the alert
    }
}


function averageRating() {
    const avgRatingElement = document.querySelector("[data-avg-rating]")

    const avgRating = parseInt(avgRatingElement.getAttribute("data-avg-rating"));

    const pRating = document.querySelector(".star-avg-rating")

    pRating.innerHTML = "";

    for (let i = 0; i < avgRating; i++) {
        pRating.innerHTML += `<label class="star-rating-label"><i class="bi bi-star-fill" style="color:gold;"></i></label>`;
    }

}


// Initialise edit button on author posts
function initEditButton() {
    // Function to edit posts
    const editButton = document.querySelector('.edit-btn');
    editButton.addEventListener('click', handleEditButton); 
}

// Function to handle edit button click and create text area, save button
function handleEditButton() {
    const recipeId = this.dataset.recipeId; 

    // Select the elements for name, description, and instructions
    const recipeNameElement = document.querySelector(`#recipe-name-${recipeId}`);
    const recipeDescriptionElement = document.querySelector(`#recipe-description-${recipeId}`);
    const recipeInstructionsElement = document.querySelector(`#recipe-instructions-${recipeId}`);
    const recipeContainer = document.querySelector('.recipe-container')

    const originalName = recipeNameElement.textContent.trim();
    const originalDescription = recipeDescriptionElement.textContent.trim();
    const originalInstructions = recipeInstructionsElement.textContent.trim();

    // Avoid re-editing if already in editing mode
    if (!recipeNameElement.querySelector('input')) { 

        // Replace content with input fields for editing
        recipeNameElement.innerHTML = `<input type="text" value="${originalName}">`;
        recipeDescriptionElement.innerHTML = `<textarea>${originalDescription}</textarea>`;
        recipeInstructionsElement.innerHTML = `<textarea>${originalInstructions}</textarea>`;

        // Create the save button
        const saveButton = document.createElement('button');
        saveButton.textContent = 'Save';
        saveButton.classList.add('btn', 'btn-success');

        // Add button to recipe container
        recipeContainer.appendChild(saveButton);

        // Handle saving the updated post
        saveButton.addEventListener('click', function() {
            const updatedName = recipeNameElement.querySelector('input').value;
            const updatedDescription = recipeDescriptionElement.querySelector('textarea').value;
            const updatedInstructions = recipeInstructionsElement.querySelector('textarea').value;

            // Send data to the backend
            fetch(`/edit_recipe/${recipeId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({
                    name: updatedName,
                    description: updatedDescription,
                    instructions: updatedInstructions
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the content in the recipe
                    recipeNameElement.innerHTML = `<h2>${data.updated_name}</h2>`;
                    recipeDescriptionElement.innerHTML = `<p>${data.updated_description}</p>`;
                    recipeInstructionsElement.innerHTML = `<p>${data.updated_instructions}</p>`;

                    // Remove the save button after saving
                    saveButton.remove();
                } else {
                    alert('Error: Could not update recipe.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while saving your recipe.');
            });
        });
    }
}
