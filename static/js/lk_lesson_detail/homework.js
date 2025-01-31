function toggleHomeworkDetails(button) {
    const homeworkPreview = button.parentElement;
    const imgElements = homeworkPreview.querySelectorAll('img');
    const description = homeworkPreview.querySelector('p');

    if (description.style.display === 'none' || description.style.display === '') {
        description.style.display = 'block';
        imgElements.forEach(img => img.style.display = 'block'); // Показываем все изображения
        button.textContent = 'Скрыть';
    } else {
        description.style.display = 'none';
        imgElements.forEach(img => img.style.display = 'none'); // Скрываем все изображения
        button.textContent = 'Моё решение';
    }
}

function updateFileNames(input) {
    const fileNames = Array.from(input.files).map(file => file.name).join(', ');
    document.getElementById('file-names').textContent = fileNames;
}
