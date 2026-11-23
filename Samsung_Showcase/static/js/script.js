function slideDown(){
    const navbar = document.getElementById("icon1");
    navbar.classList.toggle("show");
}
function togglemenu(menuId){
    const selectedMenu = document.getElementById(menuId);
    const allMenus = document.querySelectorAll(".menu");
    allMenus.forEach(menu => {
        if(menu !== selectedMenu){
            menu.classList.remove("show");
        }
        
    });
    
    selectedMenu.classList.toggle("show");
}
document.addEventListener("click", function(event) {
    if (!event.target.closest(".nav-item")) {
        document.querySelectorAll(".menu").forEach(menu => {
            menu.classList.remove("show");
        });
    }
});