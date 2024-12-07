function generateRandomColor() {
    const randomColor = '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');
    return randomColor;
}

function applyRandomColors() {
    const root = document.documentElement;

    // Генерация случайных цветов для каждой переменной
    root.style.setProperty('--background-header', generateRandomColor());
    root.style.setProperty('--background-intro', generateRandomColor());
    root.style.setProperty('--background-center-info', generateRandomColor());
    root.style.setProperty('--background-features', generateRandomColor());
    root.style.setProperty('--background-gallery', generateRandomColor());
    root.style.setProperty('--background-knowledge', generateRandomColor());
    root.style.setProperty('--background-subscribe', generateRandomColor());
    root.style.setProperty('--background-footer', generateRandomColor());
}

// Запускаем функцию на загрузке страницы
document.addEventListener('DOMContentLoaded', applyRandomColors);
