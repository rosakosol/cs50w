document.addEventListener("DOMContentLoaded", function() {
    starRating();
    fadeMessage();
    showFilterForm();
    averageRating();
    existingRating();
    initEditButton();
    initDeleteButton();
    handleRecipeIngredientFormset();
});

// Function to colour rating stars when clicked
function starRating() {
    const stars = document.querySelectorAll(".star-rating-input");
    const labels = document.querySelectorAll(".star-rating-label");

    // Click event: Mark stars gold up to the clicked star
    stars.forEach((star, index) => {
        star.addEventListener("click", function() {
            // Colour the stars gold up to and including the clicked one
            for (let i = 0; i <= index; i++) {
                labels[i].style.color = "gold"; 
            }

            // Reset the colours for the rest of the stars
            for (let i = index + 1; i < stars.length; i++) {
                labels[i].style.color = "#ccc";
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
        // Add "hide" class to the message after 3 seconds
        setTimeout(function() {
            message.classList.add("hide");

            // Add "move-up" class to the star rating container after the message fades
            setTimeout(function() {
                starRatingContainer.classList.add("move-up");
            }, 250); // Match the fade duration of the alert (250ms delay)

        }, 3000); // Wait 3 seconds before hiding the alert
    }
}

function showFilterForm() {
    const filterForm = document.querySelector(".filter-content")
    const filterButton = document.querySelector(".filter-btn")
    if (filterButton) {
        filterButton.addEventListener("click", function() {
            if (filterForm.style.display == "block") {
                filterForm.style.display = "none"
                filterButton.innerHTML = `<i class="bi bi-funnel"></i>`
            } else {
                filterForm.style.display = "block"
                filterButton.innerHTML = `<i class="bi bi-funnel-fill"></i>`
            }
        })
    }
}


function averageRating() {
    var avgRatingElements = document.querySelectorAll("[data-avg-rating]"); 

    avgRatingElements.forEach(function(avgRatingElement, index) {
        var avgRating = parseFloat(avgRatingElement.getAttribute("data-avg-rating"));

        // Select the correct pRating element based on the index
        var pRating = document.querySelectorAll(".star-avg-rating")[index]; 

        // Clear the current content inside the pRating element
        pRating.innerHTML = "";

        if (!isNaN(avgRating) && avgRating > 0) {
            // Loop to create the stars based on the avgRating value
            for (let i = 0; i < avgRating; i++) {
                pRating.innerHTML += `<label class="star-rating-label"><i class="bi bi-star-fill" style="color:gold;"></i></label>`;
            }

            // Handle half-stars if decimals
            if (avgRating % 1 !== 0) {
                pRating.innerHTML += `<label class="star-rating-label"><i class="bi bi-star-half" style="color:gold;"></i></label>`;
            }

            // Fill remaining stars if any
            for (let i = Math.ceil(avgRating); i < 5; i++) {
                pRating.innerHTML += `<label class="star-rating-label"><i class="bi bi-star" style="color:gold;"></i></label>`;
            }
        }
    });
}

function existingRating() {
    // Get the existing rating from the data attribute
    var existingRatingElement = document.querySelector("[data-avg-rating]");

    if (existingRatingElement) {
        var existingRating = parseInt(existingRatingElement.getAttribute("data-avg-rating"));
    }

    const ratingForm = document.querySelector(".form-group")

    if (ratingForm) {
        const stars = document.querySelectorAll(".star-rating-input");
        const labels = ratingForm.querySelectorAll(".star-rating-label");

        // Click event: Mark stars gold up to current rating
        for (let i = 0; i < existingRating; i++) {
            labels[i].style.color = "gold"; 
        }
    }


}





// Initialise edit button on author posts
function initEditButton() {
    // Function to edit posts
    const editButton = document.querySelector(".edit-btn")

    if (editButton) {
        editButton.addEventListener("click", handleEditButton); 
    }

}


// Function to handle edit button click and create text area, save button
function handleEditButton() {
    const recipeId = this.dataset.recipeId; 

    // Select the elements for name, description, and instructions
    var recipeNameElement = document.querySelector(`#recipe-name-${recipeId}`);
    var recipeDescriptionElement = document.querySelector(`#recipe-description-${recipeId}`);
    var recipeInstructionsElement = document.querySelector(`#recipe-instructions-${recipeId}`);
    var recipeContentContainer = document.querySelector(".recipe-content-container");

    var originalName = recipeNameElement.textContent.trim();

    // Avoid re-editing if already in editing mode
    if (!recipeNameElement.querySelector("input")) { 
        
        // Replace content with input fields for editing
        recipeNameElement.innerHTML = `<input type="text" value="${originalName}">`;

        // Initialize Quill text editors
        let quill1 = new Quill('.description-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['bold', 'italic', 'underline'],
                    ['link'],
                    ['blockquote'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'script': 'sub' }, { 'script': 'super' }],
                    ['image', 'video'],
                    ['clean']
                ]
            }
        });

        let quill2 = new Quill('.instructions-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': '1' }, { 'header': '2' }, { 'font': [] }],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['bold', 'italic', 'underline'],
                    ['link'],
                    ['blockquote'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'script': 'sub' }, { 'script': 'super' }],
                    ['image', 'video'],
                    ['clean']
                ]
            }
        });
        

        // Create the save button
        const saveButton = document.createElement("button");
        saveButton.textContent = "Save";
        saveButton.classList.add("btn", "btn-success");

        // Add button to recipe container
        recipeContentContainer.appendChild(saveButton);

        // Handle saving the updated post
        saveButton.addEventListener("click", function() {
            var updatedName = recipeNameElement.querySelector("input").value;

            // Get the HTML content from the Quill editor
            var updatedDescription = quill1.root.innerHTML
            var updatedInstructions = quill2.root.innerHTML

            // Send data to the backend
            fetch(`/edit_recipe/${recipeId}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
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
                    recipeDescriptionElement.innerHTML = data.updated_description;
                    recipeInstructionsElement.innerHTML = data.updated_instructions;

                    // Remove the save button after saving
                    saveButton.remove();
                } else {
                    alert("Error: Could not update recipe.");
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("An error occurred while saving your recipe.");
            });
        });
    }
}


// Initialise the delete button click event
function initDeleteButton() {
    const deleteButton = document.querySelector(".delete-btn");

    if (deleteButton) {
        deleteButton.addEventListener("click", handleDeleteButton);
    }

}

// Ensure delete button is initialised
document.addEventListener("DOMContentLoaded", initDeleteButton);


function handleDeleteButton() {
    const recipeId = this.dataset.recipeId;

    if (confirm("Are you sure you want to delete this recipe?")) {
        fetch(`/delete_recipe/${recipeId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Recipe deleted successfully.");
                // Redirect to index page
                window.location.href = "/";
            } else {
                alert("Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("An error occurred while deleting the recipe.");
        });
    }
}


function handleRecipeIngredientFormset() {
    const ingredientContainer = document.querySelector("#ingredient-container");
    const addIngredientButton = document.querySelector("#add-ingredient");

    if (addIngredientButton) {
        addIngredientButton.addEventListener("click", function() {
            const totalForms = document.querySelector("#id_recipe_ingredients-TOTAL_FORMS");
            const currentFormCount = parseInt(totalForms.value);
            const newFormCount = currentFormCount + 1;
    
            const newFormHtml = `
                <div class="ingredient-form form-group d-flex m-0 align-items-end" data-id="${newFormCount}">
                    ${document.querySelector(".ingredient-form").innerHTML
                        .replace(/id_recipe_ingredients-0-/g, `id_recipe_ingredients-${currentFormCount}-`)
                        .replace(/recipe_ingredients-0-/g, `recipe_ingredients-${currentFormCount}-`)
                        .replace(/data-id="1"/g, `data-id="${newFormCount}"`)}                
                </div>
            `;
    
            ingredientContainer.insertAdjacentHTML("beforeend", newFormHtml);
    
            totalForms.value = currentFormCount + 1;
        });
    
        ingredientContainer.addEventListener("click", function(event) {
            if (event.target && event.target.classList.contains("remove-ingredient")) {
                const totalForms = document.querySelector("#id_recipe_ingredients-TOTAL_FORMS");
                totalForms.value = parseInt(totalForms.value)

                // Users can only delete ingredients if there is at least 1 ingredient form in recipe form
                if (totalForms.value > 1) {
                    const formId = event.target.dataset.id;
                    const formToRemove = document.querySelector(`.ingredient-form[data-id="${formId}"]`)
                    formToRemove.remove();
                    totalForms.value = parseInt(totalForms.value) - 1;
                }
                else {
                    alert("Recipe must have at least one ingredient!"); 
                }
                

            }
        })
    }
}