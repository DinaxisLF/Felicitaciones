document.getElementById('uploadForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    let formData = new FormData();
    let fileInput = document.getElementById('file');
    
    if (fileInput.files.length > 0) {
        formData.append('file', fileInput.files[0]);

        // Make the POST request to upload the file
        fetch('/api/docentes', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.exito) {
                alert('Docentes registrados exitosamente');
                // Optionally, close the modal after success
                $('#uploadDocentes').modal('hide'); // Close the modal
                fetchDocentes(currentPage); // Refresh the table
            } else {
                alert('Error al registrar docentes: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al procesar el archivo');
        });
    } else {
        alert('Por favor selecciona un archivo');
    }
});

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}