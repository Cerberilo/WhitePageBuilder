document.addEventListener("DOMContentLoaded", function () {
    const cookieBanner = document.getElementById("cookie-banner");
    const acceptButton = document.getElementById("accept-cookies");

    // Проверяем, была ли кука уже принята
    if (!getCookie("cookiesAccepted")) {
        cookieBanner.style.display = "block"; // Показываем баннер
    }

    // Обработчик для кнопки "Принять"
    acceptButton.addEventListener("click", function () {
        setCookie("cookiesAccepted", "true", 30); // Устанавливаем куку на 30 дней
        cookieBanner.style.display = "none"; // Скрываем баннер
    });

    // Функция для установки куки
    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        document.cookie = `${name}=${value};expires=${date.toUTCString()};path=/`;
    }

    // Функция для получения куки
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(";").shift();
    }
});
