// lyaka_platform/static/js/script.js

document.addEventListener("DOMContentLoaded", function() {
    // Flash messages fade out
    const flashMessages = document.querySelector(".flash-messages");
    if (flashMessages) {
        setTimeout(() => {
            flashMessages.style.opacity = "0";
            flashMessages.style.transition = "opacity 0.5s ease-out";
            setTimeout(() => flashMessages.remove(), 500); // Remove after transition
        }, 5000); // Fade out after 5 seconds
    }

    // Add any other global JavaScript functionality here
    // For example, responsive navigation toggle for smaller screens
    // const navToggle = document.querySelector(".nav-toggle");
    // const navMenu = document.querySelector(".nav-menu");
    // if (navToggle && navMenu) {
    //     navToggle.addEventListener("click", () => {
    //         navMenu.classList.toggle("active");
    //     });
    // }
});
