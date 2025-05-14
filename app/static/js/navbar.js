document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.getElementById('navToggle');
    const navbar = document.getElementById('navbar');
    
    // Set initial state based on screen width
    let isOpen = window.innerWidth >= 768;
    updateNavbarState();

    function updateNavbarState() {
        if (isOpen) {
            navbar.classList.remove('-translate-x-full');
            navArrow.style.transform = 'rotate(180deg)';
        } else {
            navbar.classList.add('-translate-x-full');
            navArrow.style.transform = 'rotate(0deg)';
        }
    }

    // Toggle navigation
    navToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        isOpen = !isOpen;
        updateNavbarState();
    });

    // Close navigation when clicking outside
    document.addEventListener('click', (e) => {
        if (isOpen && !navbar.contains(e.target) && e.target !== navToggle) {
            isOpen = false;
            updateNavbarState();
        }
    });

});
