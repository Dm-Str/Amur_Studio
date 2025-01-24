// ... существующий код ...
// Исправить положения ползунка. Должен сохранять последнюю позицую и начинать двигаться от нее
document.addEventListener("DOMContentLoaded", function() {
    // Восстановление положения прокрутки
    const scrollPosition = sessionStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, parseInt(scrollPosition));
    }

    // Получаем текущий урок по его id
    const currentLessonId = document.body.getAttribute('data-current-lesson-id');
    const currentLessonElement = document.getElementById("lesson-" + currentLessonId);

    if (currentLessonElement) {
        currentLessonElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Сохранение положения прокрутки перед переходом на следующий урок
    window.addEventListener('beforeunload', function() {
        sessionStorage.setItem('scrollPosition', window.scrollY);
    });
});

// ... существующий код ...


// document.addEventListener("DOMContentLoaded", function() {
//     // Восстановление положения прокрутки
//     const scrollPosition = sessionStorage.getItem('scrollPosition');
//     console.log("Restored scroll position:", scrollPosition); // Проверка восстановленного значения
//     if (scrollPosition) {
//         window.scrollTo(0, parseInt(scrollPosition));
//     }
//
//     // Получаем текущий урок по его id
//     const currentLessonId = document.body.getAttribute('data-current-lesson-id');
//     const currentLessonElement = document.getElementById("lesson-" + currentLessonId);
//
//     if (currentLessonElement) {
//         currentLessonElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
//     }
//
//     // Сохранение положения прокрутки перед переходом на следующий урок
//     window.addEventListener('beforeunload', function() {
//         console.log("Saved scroll position:", window.scrollY); // Проверка сохраняемого значения
//         sessionStorage.setItem('scrollPosition', window.scrollY);
//     });
// });
//
// document.addEventListener("DOMContentLoaded", function() {
//     // Восстановление положения прокрутки
//     const scrollPosition = sessionStorage.getItem('scrollPosition');
//     if (scrollPosition) {
//         window.scrollTo(0, parseInt(scrollPosition));
//     }
//
//     // Получаем текущий урок по его id
//     const currentLessonId = document.body.getAttribute('data-current-lesson-id');
//     const currentLessonElement = document.getElementById("lesson-" + currentLessonId);
//
//     if (currentLessonElement) {
//         currentLessonElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
//     }
//
//     // Сохранение положения прокрутки перед переходом на следующий урок
//     window.addEventListener('beforeunload', function() {
//         sessionStorage.setItem('scrollPosition', window.scrollY);
//     });
// });
