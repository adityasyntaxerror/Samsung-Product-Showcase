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
function slideDown() {
    const dropdown = document.getElementById("icon1");
    if (dropdown) dropdown.classList.toggle("show");
}

function togglemenu(menuId) {
    const selectedMenu = document.getElementById(menuId);
    document.querySelectorAll(".menu").forEach(menu => {
        if (menu !== selectedMenu) menu.classList.remove("show");
    });
    selectedMenu.classList.toggle("show");
}

// Mobile hamburger (new)
function toggleMobileMenu() {
    const nav = document.getElementById("main-navigation");
    nav.classList.toggle("open");
    if (!nav.classList.contains("open")) {
        document.querySelectorAll(".menu").forEach(m => m.classList.remove("show"));
    }
}

// Close menus when clicking outside
document.addEventListener("click", function (event) {
    if (!event.target.closest(".nav-item")) {
        document.querySelectorAll(".menu").forEach(menu => menu.classList.remove("show"));
    }
    if (!event.target.closest(".user-menu")) {
        const dropdown = document.getElementById("icon1");
        if (dropdown) dropdown.classList.remove("show");
    }
});

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        document.querySelectorAll(".menu, .dropdown").forEach(el => el.classList.remove("show"));
    }
});
