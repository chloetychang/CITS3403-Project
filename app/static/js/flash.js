// Automatically hide flash messages after 5 seconds
setTimeout(() => {
    const flashMessages = document.querySelector('.absolute.top-4');
    if (flashMessages) {
        flashMessages.style.transition = 'opacity 0.5s ease';
        flashMessages.style.opacity = '0';
        setTimeout(() => flashMessages.remove(), 500); // Remove from DOM after fade-out
    }
}, 5000); // 5000ms = 5 seconds

// Function to dismiss flash messages manually
function dismissFlashMessage(button) {
    const flashMessage = button.parentElement;
    flashMessage.style.transition = 'opacity 0.5s ease';
    flashMessage.style.opacity = '0';
    setTimeout(() => flashMessage.remove(), 500); // Remove from DOM after fade-out
}