// Make functions globally available
function openPopup() {
    document.getElementById("popup").classList.remove("hidden");
}

function closePopup() {
    document.getElementById("popup").classList.add("hidden");
}

function clearForm() {
    const fields = ['entry_date_sleep', 'sleep_time', 'entry_date_wake', 'wake_time', 'mood'];
    fields.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.value = '';
    });
}

// Add event listeners when DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
    console.log("sleep.js loaded");
});