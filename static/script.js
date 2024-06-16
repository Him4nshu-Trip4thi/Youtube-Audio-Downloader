document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    const urlInput = document.getElementById('url');
    const dialogueBox = document.querySelector('.dialogue-box');
    const previewImage = document.getElementById('preview-image');
    const downloadButton = document.getElementById('download-button');

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        const url = urlInput.value;
        if (url) {
            fetch(`https://noembed.com/embed?url=${url}`)
                .then(response => response.json())
                .then(data => {
                    if (data.thumbnail_url) {
                        previewImage.src = data.thumbnail_url;
                        dialogueBox.style.display = 'block';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    });

    downloadButton.addEventListener('click', function () {
        form.submit();
    });
});
