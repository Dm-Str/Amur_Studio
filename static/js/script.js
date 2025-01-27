// document.getElementById('registration-form').addEventListener('submit', function (event) {
//     event.preventDefault();
//     alert('Форма регистрации отправлена!');
// });
//
// document.getElementById('login-form').addEventListener('submit', function (event) {
//     event.preventDefault();
//     alert('Форма авторизации отправлена!');
// });
//
//
// document.addEventListener('DOMContentLoaded', function () {
//     console.log("DOM полностью загружен"); // Отладочное сообщение
//     document.getElementById('profile-toggle').addEventListener('click', function (event) {
//         event.preventDefault(); // Предотвращаем переход по ссылке
//         const menu = document.getElementById('profile-menu');
//         console.log("Кнопка нажата"); // Отладочное сообщение
//         menu.style.display = menu.style.display === 'none' ? 'block' : 'none'; // Переключаем видимость меню
//     });
// });
//
// // Пример массива курсов пользователя
// const userCourses = []; // Здесь могут быть курсы пользователя
//
// // Функция для отображения информации о курсах
// function displayCourses() {
//     const courseContainer = document.getElementById('courseContainer');
//
//     if (userCourses.length === 0) {
//         // Если у пользователя нет курсов
//         courseContainer.innerHTML = '<button onclick="selectCourse()">Выбрать курс</button>';
//     } else {
//         // Если у пользователя есть курсы
//         const courseList = userCourses.map(course => `<li>${course}</li>`).join('');
//         courseContainer.innerHTML = `<ul>${courseList}</ul>`;
//     }
// }
//
// // Функция для выбора курса
// function selectCourse() {
//     // Логика для выбора курса
//     alert('Открыть выбор курсов');
// }
//
// // Вызов функции для отображения курсов
// displayCourses();



