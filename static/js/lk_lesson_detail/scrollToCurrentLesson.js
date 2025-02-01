
function goToNextLesson(nextLessonUrl) {
    // Сохраняем текущую позицию прокрутки
    localStorage.setItem('scrollPosition', window.scrollY);
    // Переход к следующему уроку
    window.location.href = nextLessonUrl;
}

document.addEventListener("DOMContentLoaded", function() {
    // Восстановление положения прокрутки
    const scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        setTimeout(function() {
            window.scrollTo(0, parseInt(scrollPosition));
            localStorage.removeItem('scrollPosition');
        }, 100);
    }

    const currentLessonId = document.body.getAttribute('data-current-lesson-id');
    const currentLessonElement = document.getElementById("lesson-" + currentLessonId);

    if (currentLessonElement) {
        currentLessonElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    } else {
        console.warn("Элемент с ID lesson-" + currentLessonId + " не найден.");
    }
});

// Debounce scroll position saving
let saveScrollTimeout;
window.addEventListener('scroll', function() {
    clearTimeout(saveScrollTimeout);
    saveScrollTimeout = setTimeout(function() {
        localStorage.setItem('scrollPosition', window.scrollY);
    }, 100);
});

// Сохранение положения прокрутки перед переходом на следующий урок
window.addEventListener('beforeunload', function() {
    localStorage.setItem('scrollPosition', window.scrollY);
});



