document.addEventListener('DOMContentLoaded', function() {
    starRating();
    fadeMessage();
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
    } else {
        console.error("Elements not found. Ensure '.alert' and '.star-rating-container' exist in the DOM.");
    }
}
