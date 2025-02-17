document.addEventListener('DOMContentLoaded', function() {
    starRating();
});


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
