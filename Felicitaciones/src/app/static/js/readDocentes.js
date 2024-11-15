const apiUrl = '/api/docentes';
let currentPage = 1;
const perPage = 4;

async function fetchDocentes(page = 1) {
    try {
        // Fetch data from API with pagination
        const response = await fetch(`${apiUrl}?page=${page}&per_page=${perPage}`);
        const data = await response.json();

        // Check if the request was successful
        if (response.ok) {
            renderTable(data.teachers);
            renderPagination(data.total_pages, data.page);
        } else {
            console.error('Error fetching docentes:', data.message);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render table rows
function renderTable(docentes) {
    const itemsList = document.getElementById('items-list');
    itemsList.innerHTML = ''; // Clear existing rows

    // Iterate through docentes data and create table rows
    docentes.forEach(docente => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${docente.ID_docente}</td>
            <td>${docente.Nombre} ${docente.Apellido}</td>
            <td>${docente.Fecha_de_Nacimiento}</td>
            <td>${docente.Correo}</td>
            <td>${docente.Estado}</td>
            <td>
                <button type="button" class="btn btn-warning btn-edit" data-bs-toggle="modal" data-bs-target="#editDocenteModal" data-id="${docente.ID_docente}">
                    <i class="fas fa-edit fa-xs"></i>
                </button>
                <button type="button" class="btn btn-danger btn-delete" data-id="${docente.ID_docente}">
                    <i class="fas fa-trash fa-xs"></i>
                </button>
            </td>
        `;
        itemsList.appendChild(row);
    });

    // Attach click event to each "Edit" button
    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", function() {
            const docenteId = this.getAttribute("data-id");
            console.log(`docenteId: ${docenteId}`); // Debugging line to log the docenteId
            
            // Check if docenteId is valid before making the API request
            if (!docenteId) {
                console.error('No docenteId found!');
                return; // Exit if no docenteId
            }
    
            fetch(`/api/docentes/${docenteId}`)
                .then(response => {
                    console.log('Response Status:', response.status); // Log the response status
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Data from API:', data); // Log the fetched data
    
                    if (data.docentes_api) {
                        const docente = data.docentes_api;
    
                        // Populate the modal fields with the docente data
                        document.getElementById("docenteId").value = docente.ID_docente;
                        document.getElementById("editNombre").value = docente.Nombre;
                        document.getElementById("editApellido").value = docente.Apellido;
                        document.getElementById("editCorreo").value = docente.Correo;
                        document.getElementById("editEstado").value = docente.Estado;
    
                        // Format Fecha_de_Nacimiento before setting it on the form
                        const formattedDate = formatDate(docente.Fecha_de_Nacimiento);
                        document.getElementById("editFechaNacimiento").value = formattedDate;
    
                        // Show the modal with the populated form
                        $('#editDocenteModal').modal('show');
                    } else {
                        alert('Docente no encontrado');
                    }
                })
                .catch(error => {
                    console.error('Error fetching docente data:', error);
                    alert('Error al obtener los datos del docente');
                });
        });
    });
    ;
}


// Add event listener to the "Guardar cambios" button
document.getElementById("editDocenteForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent the form from submitting the default way

    // Get the form data
    const docenteId = document.getElementById("docenteId").value;
    const nombre = document.getElementById("editNombre").value;
    const apellido = document.getElementById("editApellido").value;
    const fechaNacimiento = document.getElementById("editFechaNacimiento").value;
    const correo = document.getElementById("editCorreo").value;
    const estado = document.getElementById("editEstado").value;

    // Create an object with the updated docente data
    const updatedDocente = {
        Nombre: nombre,
        Apellido: apellido,
        Fecha_de_Nacimiento: fechaNacimiento,
        Correo: correo,
        Estado: estado
    };

    // Send the PUT request to the API
    fetch(`/api/docentes/${docenteId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedDocente), // Send the updated data in the body of the request
    })
    .then(response => response.json())
    .then(data => {
        if (data.exito) {
            // If the update was successful, close the modal and refresh the table
            alert("Docente actualizado con éxito!");
            $('#editDocenteModal').modal('hide'); // Close the modal
            fetchDocentes(currentPage); // Refresh the table
        } else {
            alert("Error al actualizar docente.");
        }
    })
    .catch(error => {
        console.error("Error al actualizar docente:", error);
        alert("Hubo un error al actualizar el docente.");
    });
});



document.addEventListener("click", function(event) {
    // Check if the clicked element is a "Delete" button
    if (event.target && event.target.matches(".btn-delete")) {
        const docenteId = event.target.getAttribute("data-id");

        // Ask for confirmation before deleting
        if (confirm("¿Estás seguro de que deseas eliminar este docente?")) {
            // Send the DELETE request to the API
            fetch(`/api/docentes/${docenteId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.exito) {
                    // If the deletion was successful, refresh the table
                    alert("Docente eliminado con éxito!");
                    fetchDocentes(currentPage); // Refresh the table after deletion
                } else {
                    alert("Error al eliminar docente.");
                }
            })
            .catch(error => {
                console.error("Error al eliminar docente:", error);
                alert("Hubo un error al eliminar el docente.");
            });
        }
    }
});

// Function to render pagination
function renderPagination(totalPages, currentPage) {
    const pagination = document.querySelector('.pagination');
    pagination.innerHTML = ''; // Clear existing pagination

    for (let i = 1; i <= totalPages; i++) {
        const pageItem = document.createElement('li');
        pageItem.classList.add('page-item');
        if (i === currentPage) pageItem.classList.add('active');
        
        const pageLink = document.createElement('a');
        pageLink.classList.add('page-link');
        pageLink.textContent = i;
        pageLink.href = '#';
        pageLink.addEventListener('click', (event) => {
            event.preventDefault();
            fetchDocentes(i);
        });

        pageItem.appendChild(pageLink);
        pagination.appendChild(pageItem);
    }
}

// Initial fetch for the first page of docentes
fetchDocentes();


function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Get month and ensure 2 digits
    const day = String(date.getDate()).padStart(2, '0'); // Get day and ensure 2 digits
    return `${year}-${month}-${day}`; // Return in the format YYYY-MM-DD
}


if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}