document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.querySelector('.forum-rules-toggle');
    const rulesContainer = document.querySelector('.forum-rules');

    toggleButton.addEventListener('click', function () {
        if (rulesContainer.style.display === 'none') {
            rulesContainer.style.display = 'block';
        } else {
            rulesContainer.style.display = 'none';
        }
    });
});
