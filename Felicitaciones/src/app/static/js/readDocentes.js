document.addEventListener("DOMContentLoaded", function() {
    // Function to fetch data from API
    fetch('/api/docentes')
    .then(response => response.json())
    .then(data => {
        const docentesArray = data[0]; // El array de docentes está en data[0]

        if (Array.isArray(docentesArray)) {
            const itemsList = document.getElementById("items-list");
            
            // Clear the itemsList in case there's any data
            itemsList.innerHTML = "";

            // Loop through each docente and create a new row in the table
            docentesArray.forEach(docente => {
                // Create a new table row
                const row = document.createElement("tr");

                // Create and append cells for each column
                const columns = ['ID_docente', 'Nombre', 'Apellido', 'Fecha_de_Nacimiento', 'Correo', 'Estado'];

                columns.forEach(column => {
                    const cell = document.createElement("td");
                    cell.textContent = docente[column];
                    row.appendChild(cell);
                });

                // Crear una celda para los botones
                const actionsCell = document.createElement("td");

                // Botón Editar
                const editButton = document.createElement("button");
                editButton.className = "btn btn-warning btn-sm me-2"; 
                editButton.textContent = "Editar";
                editButton.addEventListener("click", function() {
                    cargarDatosDocente(docente.ID_docente, docente.Nombre, docente.Apellido, docente.Fecha_de_Nacimiento, docente.Correo, docente.Estado);
                });
                actionsCell.appendChild(editButton);

                // Botón Eliminar
                const deleteButton = document.createElement("button");
                deleteButton.className = "btn btn-danger btn-sm";
                deleteButton.textContent = "Eliminar";
                 // Evento para Eliminar Docente
                 deleteButton.addEventListener("click", function() {
                    eliminarDocente(docente.ID_docente); 
                });
                actionsCell.appendChild(deleteButton);

                // Añadir la celda de acciones a la fila
                row.appendChild(actionsCell);

                // Append the row to the items list
                itemsList.appendChild(row);
            });
        } else {
            console.error("Unexpected data format:", data);
        }
    })
    .catch(error => {
        console.error("Error fetching data:", error);
    });
});
