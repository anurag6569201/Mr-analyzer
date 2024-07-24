document.getElementById('id_pdf_file').addEventListener('change', function(event) {
    if (event.target.files.length > 0) {
        document.getElementById('form-submitted-btn').click()
    }
});

function toggleFullScreen() {
    const chatBox = document.getElementById('page-content');
    const fullscreenButton = document.getElementById('fullscreen-button');

    if (!document.fullscreenElement) {
        chatBox.requestFullscreen().catch(err => {
            console.log(`Error attempting to enable full-screen mode: ${err.message}`);
        });
        fullscreenButton.textContent = 'Exit';
    } else {
        if (document.exitFullscreen) {
            document.exitFullscreen();
        }
        fullscreenButton.textContent = 'Full Screen';
    }
}