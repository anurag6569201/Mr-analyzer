document.getElementById('id_pdf_file').addEventListener('change', function(event) {
    if (event.target.files.length > 0) {
        document.getElementById('form-submitted-btn').click()
        document.getElementById('uploading-file').style.display = 'none';
        document.getElementById('conversations').style.display = 'flex';
    }
});