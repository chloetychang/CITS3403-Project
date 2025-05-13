document.addEventListener("DOMContentLoaded", function() {
    // For 'Close Form' Button
    function openPopup() {
    document.getElementById("popup").classList.remove("hidden");
    }

    function closePopup() {
    document.getElementById("popup").classList.add("hidden");
    }

    // For 'Clear Form' Button
    function clearForm() {
    const fields = ['entry_date_sleep', 'sleep_time', 'entry_date_wake', 'wake_time', 'mood'];
    fields.forEach(id => {
        const element = document.getElementById(id);
        if (element) element.value = ''; // If element exists on the page, clear its value
    });
    }
});