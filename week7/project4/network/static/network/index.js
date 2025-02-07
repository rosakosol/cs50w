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

});