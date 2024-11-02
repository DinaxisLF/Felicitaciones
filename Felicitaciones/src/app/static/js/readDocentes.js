document.addEventListener("DOMContentLoaded", function () {

    fetch('/api/docentes')
        .then(response => response.json())
        .then(data => {
            const docentesArray = data[0]; 

            if (Array.isArray(docentesArray)) {
                const itemsList = document.getElementById("items-list");

                itemsList.innerHTML = "";

                docentesArray.forEach(docente => {

                    const row = document.createElement("tr");


                    const columns = ['ID_docente', 'Nombre', 'Apellido', 'Fecha_de_Nacimiento', 'Correo', 'Estado'];

                    columns.forEach(column => {
                        const cell = document.createElement("td");
                        cell.textContent = docente[column];
                        row.appendChild(cell);
                    });


                    const actionsCell = document.createElement("td");

                    // Botón Editar
                    const editButton = document.createElement("button");
                    editButton.className = "btn btn-warning btn-sm me-2";
                    editButton.textContent = "Editar";
                    editButton.addEventListener("click", function () {
                        cargarDatosDocente(docente.ID_docente, docente.Nombre, docente.Apellido, docente.Fecha_de_Nacimiento, docente.Correo, docente.Estado);
                    });
                    actionsCell.appendChild(editButton);

                    const divider = document.createElement("hr");

                    actionsCell.appendChild(divider);

                    // Botón Eliminar
                    const deleteButton = document.createElement("button");
                    deleteButton.className = "btn btn-danger btn-sm";
                    deleteButton.textContent = "Eliminar";
                    // Evento para Eliminar Docente
                    deleteButton.addEventListener("click", function () {
                        eliminarDocente(docente.ID_docente);
                    });
                    actionsCell.appendChild(deleteButton);

    
                    row.appendChild(actionsCell);


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
