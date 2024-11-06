function filtrarDocentes(page = 1) {
    const nombre = document.getElementById("nombre").value;
    const estado = document.getElementById("estado").value;
    const mesNacimiento = document.getElementById("mesNacimiento").value;

    fetch(`/filtrar_docentes?nombre=${nombre}&estado=${estado}&mesNacimiento=${mesNacimiento}&page=${page}&per_page=${perPage}`)
        .then(response => response.json())
        .then(data => {
            const docentesArray = data.teachers;
            const itemsList = document.getElementById("items-list");
            itemsList.innerHTML = "";

            if (Array.isArray(docentesArray)) {
                docentesArray.forEach(docente => {
                    const row = document.createElement("tr");
                    const columns = ['ID_docente', 'Nombre', 'Apellido', 'Fecha_de_Nacimiento', 'Correo', 'Estado'];
                    columns.forEach(column => {
                        const cell = document.createElement("td");
                        cell.textContent = docente[column];
                        row.appendChild(cell);
                    });

                    const actionsCell = document.createElement("td");
                    const editButton = document.createElement("button");
                    editButton.className = "btn btn-warning btn-sm me-2";
                    editButton.textContent = "Editar";
                    editButton.addEventListener("click", function () {
                        cargarDatosDocente(docente.ID_docente, docente.Nombre, docente.Apellido, docente.Fecha_de_Nacimiento, docente.Correo, docente.Estado);
                    });
                    actionsCell.appendChild(editButton);

                    const divider = document.createElement("hr");
                    divider.style.margin = "0.5rem 0"; 
                    actionsCell.appendChild(divider);

                    const deleteButton = document.createElement("button");
                    deleteButton.className = "btn btn-danger btn-sm";
                    deleteButton.textContent = "Eliminar";
                    deleteButton.addEventListener("click", function () {
                        eliminarDocente(docente.ID_docente);
                    });
                    actionsCell.appendChild(deleteButton);

                    row.appendChild(actionsCell);
                    itemsList.appendChild(row);
                });

                actualizarPaginacion(data.page, data.total_pages); 
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
}

document.getElementById("buscar-docentes-btn").addEventListener("click", function() {
    filtrarDocentes(); 
});


function reiniciarFiltros() {
    document.getElementById("nombre").value = "";
    document.getElementById("estado").value = "";
    document.getElementById("mesNacimiento").value = "";
    cargarDocentes(1); 
}

const reiniciarBtn = document.getElementById("reiniciarBtn");
if (reiniciarBtn) {
    reiniciarBtn.addEventListener("click", reiniciarFiltros);
}
