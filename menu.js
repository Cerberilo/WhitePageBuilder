document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.querySelector(".menu-toggle");
    const mobileMenu = document.querySelector(".mobile-menu");
    const menuClose = document.querySelector(".menu-close");

    if (menuToggle && mobileMenu && menuClose) {
        // Открытие меню
        menuToggle.addEventListener("click", function () {
            mobileMenu.classList.add("open");
        });

        // Закрытие меню
        menuClose.addEventListener("click", function () {
            mobileMenu.classList.remove("open");
        });

        // Закрытие меню при клике вне его области
        document.addEventListener("click", function (event) {
            if (!mobileMenu.contains(event.target) && !menuToggle.contains(event.target)) {
                mobileMenu.classList.remove("open");
            }
        });
    } else {
        console.error("Элементы меню не найдены.");
    }
});

