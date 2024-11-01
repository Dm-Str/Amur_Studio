document.getElementById('registration-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Форма регистрации отправлена!');
});

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Форма авторизации отправлена!');
});
