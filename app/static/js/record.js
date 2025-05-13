// Define functions in global scope so they're accessible from HTML
function openPopup(year, month, day) {
    console.log("Opening popup for:", year, month, day);
    
    const popup = document.getElementById("recordPopup");
    const modalDate = document.getElementById("modalDate");
    const modalContent = document.getElementById("modalContent");

    // Check if elements exist
    if (!popup || !modalDate || !modalContent) {
        console.error("Required DOM elements not found");
        return;
    }

    // Convert parameters to strings and pad with zeros
    const paddedMonth = String(month).padStart(2, '0');
    const paddedDay = String(day).padStart(2, '0');
    const formattedDate = `${year}-${paddedMonth}-${paddedDay}`;

    modalDate.textContent = formattedDate;
    modalContent.innerHTML = "Loading...";

    popup.classList.remove("hidden");

    fetch(`/get_sleep_data?date=${formattedDate}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.length === 0) {
                modalContent.innerHTML = `
                    <p>No records found.</p>
                    <div class="mt-4">
                        <a href="/sleep" class="bg-green-500 text-white py-1 px-3 rounded text-sm transition-colors duration-200">
                            Add Sleep Entry
                        </a>
                    </div>
                `;
            } else {
                modalContent.innerHTML = data.map(entry => `
                    <div class="mb-2 border-b pb-2">
                        <p><strong>Sleep Date:</strong> ${entry.sleep_date}</p>
                        <p><strong>Sleep Time:</strong> ${entry.sleep_time}</p>
                        <p><strong>Wake Date:</strong> ${entry.wake_date || "N/A"}</p>
                        <p><strong>Wake Time:</strong> ${entry.wake_time || "N/A"}</p>
                        <p><strong>Sleep Duration:</strong> ${entry.sleep_duration || "N/A"}</p>
                        <p><strong>Mood:</strong> ${entry.mood}</p>
                        <div class="mt-3 text-right">
                            <button onclick="deleteEntry(${entry.entry_id})" 
                                class="bg-red-500 text-white py-1 px-3 rounded text-sm transition-colors duration-200">
                                Delete Entry
                            </button>
                        </div>
                    </div>
                `).join('');
            }
        })
        .catch(err => {
            console.error("Error fetching data:", err);
            modalContent.innerHTML = "<p>Error loading data. Please try again later.</p>";
        });
}

function closePopup() {
    const popup = document.getElementById("recordPopup");
    if (popup) {
        popup.classList.add("hidden");
    } else {
        console.error("Popup element not found");
    }
}

function deleteEntry(entryId) {
    if (!entryId) {
        console.error("No entry ID provided");
        return;
    }

    if (confirm("Are you sure you want to delete this sleep entry? This action cannot be undone.")) {
        fetch(`/delete_sleep_entry/${entryId}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrf_token
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Error deleting entry');
                });
            }
            return response.json();
        })
        .then(() => {
            alert("Entry deleted successfully");
            closePopup();
            location.reload();
        })
        .catch(error => {
            console.error('Error:', error);
            alert(error.message || "An error occurred while deleting the entry");
        });
    }
}

// Add initialization code when DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
    console.log("Sleep record functionality initialized");
    
    // Add click event listener to close popup when clicking outside
    const popup = document.getElementById("recordPopup");
    if (popup) {
        popup.addEventListener("click", function(event) {
            if (event.target === popup) {
                closePopup();
            }
        });
    }
});