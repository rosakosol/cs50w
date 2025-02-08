document.addEventListener('DOMContentLoaded', function() {

    // Function to like post
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const postId = this.getAttribute('data-post-id');

            try {
                const response = await fetch(`/like/${postId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        post_id: postId
                    })
                });

                const data = await response.json();

                const likeCountElement = document.getElementById(`like-count-${postId}`);
                const button = this;
        
                if (data.liked) {
                    button.textContent = 'Unlike';
                } else {
                    button.textContent = 'Like';
                }
        
                likeCountElement.textContent = data.like_count;
            } catch (error) {
                console.error('Error with Like', error);
            }
        })
    })

    // Follow button functionality (fixed for multiple buttons)
    const followButtons = document.querySelectorAll('.follow-btn'); // Select all follow buttons

    followButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const profileUsername = this.getAttribute('data-profile-username');

            try {
                const response = await fetch(`/follow/${profileUsername}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();

                // Get the follow count element
                const followCountElement = document.getElementById(`follow-count-${profileUsername}`);
                const buttonText = this.querySelector('p');
    
                // Update the button text based on whether it's followed or not
                if (data.followed) {
                    buttonText.textContent = 'Unfollow';
                } else {
                    buttonText.textContent = 'Follow';
                }

                // Update the follower count displayed on the page
                followCountElement.textContent = `Followers: ${data.follow_count}`;
            } catch (error) {
                console.error('Error with Follow', error);
            }
        });
    });

});
