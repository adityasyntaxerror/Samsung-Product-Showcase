// Mobile navigation: toggle the menu and keep aria-expanded in sync.
document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.querySelector(".menu-toggle");
    const navigation = document.querySelector(".main-navigation");
    if (!toggle || !navigation) return;

    toggle.addEventListener("click", () => {
        const open = navigation.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
});
