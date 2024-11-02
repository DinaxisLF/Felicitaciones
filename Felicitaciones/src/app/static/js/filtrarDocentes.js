async function filtrarDocentes() {
    const nombre = document.getElementById("nombre").value;
    const estado = document.getElementById("estado").value;
    const mesNacimiento = document.getElementById("mesNacimiento").value;

    const url = `/filtrar_docentes?nombre=${nombre}&estado=${estado}&mesNacimiento=${mesNacimiento}`;

    try {
        const response = await fetch(url);
        const docentes = await response.json();

        const tablaBody = document.getElementById("items-list");
        tablaBody.innerHTML = "";

        docentes.forEach(docente => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${docente.ID_docente}</td>
                <td>${docente.Nombre}</td>
                <td>${docente.Apellido}</td>
                <td>${new Date(docente.Fecha_de_Nacimiento).toDateString()}</td>
                <td>${docente.Correo}</td>
                <td>${docente.Estado}</td> 
                <td>
                    <button class="btn btn-warning btn-edit" data-id="${docente.ID_docente}">Editar</button>
                    <hr>
                    <button class="btn btn-danger btn-delete" data-id="${docente.ID_docente}">Eliminar</button>
                </td>
            `;
            tablaBody.appendChild(row);

            const editButton = row.querySelector(".btn-edit");
            editButton.addEventListener("click", function () {
                cargarDatosDocente(docente.ID_docente, docente.Nombre, docente.Apellido, docente.Fecha_de_Nacimiento, docente.Correo, docente.Estado);
            });

            const deleteButton = row.querySelector(".btn-delete");
            deleteButton.addEventListener("click", function () {
                eliminarDocente(docente.ID_docente);
            });
        });
    } catch (error) {
        console.error("Error al obtener los datos:", error);
    }
}

async function reiniciarFiltros() {

    document.getElementById("nombre").value = "";
    document.getElementById("estado").value = "";
    document.getElementById("mesNacimiento").value = "";

    try {
        const response = await fetch('/filtrar_docentes'); 
        const docentes = await response.json();

        const tablaBody = document.getElementById("items-list");
        tablaBody.innerHTML = "";

        docentes.forEach(docente => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${docente.ID_docente}</td>
                <td>${docente.Nombre}</td>
                <td>${docente.Apellido}</td>
                <td>${new Date(docente.Fecha_de_Nacimiento).toDateString()}</td>
                <td>${docente.Correo}</td>
                <td>${docente.Estado}</td> 
                <td>
                    <button class="btn btn-warning btn-edit" data-id="${docente.ID_docente}">Editar</button>
                    <button class="btn btn-danger btn-delete" data-id="${docente.ID_docente}">Eliminar</button>
                </td>
            `;
            tablaBody.appendChild(row);

            const editButton = row.querySelector(".btn-edit");
            editButton.addEventListener("click", function () {
                cargarDatosDocente(docente.ID_docente, docente.Nombre, docente.Apellido, docente.Fecha_de_Nacimiento, docente.Correo, docente.Estado);
            });

            const deleteButton = row.querySelector(".btn-delete");
            deleteButton.addEventListener("click", function () {
                eliminarDocente(docente.ID_docente);
            });
        });
    } catch (error) {
        console.error("Error al obtener los datos:", error);
    }
}