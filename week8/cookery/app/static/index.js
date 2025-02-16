document.addEventListener('DOMContentLoaded', function() {
    starRating();
});



function starRating() {
    const stars = document.querySelectorAll(".star-rating-input");
    const labels = document.querySelectorAll(".star-rating-label");

    labels.forEach((label, index) => {
        label.addEventListener("mouseover", function() {
            for (let i = 0; i <= index; i++) {
                labels[i].style.color = "gold";
            }
        });

        label.addEventListener("mouseout", function() {
            for (let i = 0; i <= stars.length; i++) {
                if (!stars[i].checked) {
                    labels[i].style.color = "#ccc";
                }
            }
        });
    });

    stars.forEach((star, index) => {
        star.addEventListener("click", function() {
            for (let i = 0; i <= index; i++) {
                labels[i].style.color = "gold";
            }

            for (let i = index + 1; i < stars.length; i++) {
                labels[i].style.color = "#ccc";
            }
        })
    });
}