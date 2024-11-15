document.getElementById('buscar-docentes-btn').addEventListener('click', function() {
    // Get filter values
    let nombre = document.getElementById('nombre').value;
    let estado = document.getElementById('estado').value;
    let mesNacimiento = document.getElementById('mesNacimiento').value;

    // Fetch the data using AJAX or a fetch request
    fetch(`/api/docentes?nombre=${nombre}&estado=${estado}&mesNacimiento=${mesNacimiento}`)
        .then(response => response.json())
        .then(data => {
            let teachers = data.teachers;
            let tableBody = document.getElementById('items-list');
            tableBody.innerHTML = ''; // Clear the table body before updating

            // Add rows to the table dynamically
            teachers.forEach(teacher => {
                let row = document.createElement('tr');
                row.innerHTML = `
                    <td>${teacher.ID_docente}</td>
                    <td>${teacher.Nombre} ${teacher.Apellido}</td>
                    <td>${teacher.Fecha_de_Nacimiento}</td>
                    <td>${teacher.Correo}</td>
                    <td>${teacher.Estado}</td>
                    <td>
                        <button type="button" class="btn btn-warning btn-edit">
                            <i class="fas fa-edit fa-xs"></i>
                        </button>
                        <button type="button" class="btn btn-danger btn-delete">
                            <i class="fas fa-trash fa-xs"></i>
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            // Handle pagination if necessary (not implemented in this example)
        })
        .catch(error => console.error('Error fetching teachers:', error));
});


function reiniciarFiltros() {
    document.getElementById('nombre').value = '';
    document.getElementById('estado').value = '';
    document.getElementById('mesNacimiento').value = '';

    // Trigger the search again after reset
    document.getElementById('buscar-docentes-btn').click();
}

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}