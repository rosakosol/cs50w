document.addEventListener('DOMContentLoaded', function() {
    // Button to add new posts, will show/hide the new post form
    const newPostButton = document.querySelector('#new-post-btn');

    if (newPostButton) {
        newPostButton.addEventListener('click', create_new_post);
    }

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
                const buttonText = this;
    
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

// Function to fade in/out the new post view on the index page
function create_new_post() {
    const createPostContainer = document.querySelector('#create-post-view');
    const allPostsContainer = document.querySelector('.all-posts-container');

    // If view is open, fade it out
    if (createPostContainer.classList.contains('fade-in-down') || createPostContainer.classList.contains(''))  {
        createPostContainer.classList.remove('fade-in-down');
        createPostContainer.classList.add('fade-out-up');

        allPostsContainer.style.marginTop = '0';
        setTimeout(function() {
            createPostContainer.style.display = 'none';
        })

    // Otherwise fade in new post view
    } else {
        createPostContainer.style.display = 'block';
        createPostContainer.classList.remove('fade-out-up');
        createPostContainer.classList.add('fade-in-down');
        allPostsContainer.style.marginTop = '200px';

    }
}