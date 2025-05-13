// CSRF Token for AJAX requests
function getCSRFToken() {
    return document.querySelector('input[name=csrf_token]').value;
}

function viewFriendData(friendId) {
    console.log("Viewing friend:", friendId);
    // Implement functionality to display friend's sleep data
    // This will be implemented later
}

function handleRequest(requestId, action) {
    // Show loading indicator or disable buttons to prevent double-clicks
    const buttons = document.querySelectorAll(`button[onclick*="${requestId}"]`);
    buttons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('opacity-50');
    });

    fetch(`/handle_friend_request/${requestId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ action: action })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server responded with an error');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Reload the page to show updated friend lists
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        // Re-enable buttons in case of error
        buttons.forEach(btn => {
            btn.disabled = false;
            btn.classList.remove('opacity-50');
        });
        
        // Show error message
        alert('There was an error processing your request. Please try again.');
    });
}

function unfriendUser(friendId) {
    if (confirm("Are you sure you want to remove this friend?")) {
        fetch(`/unfriend/${friendId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server responded with an error');
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
            window.location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error removing this friend. Please try again.');
        });
    }
}

