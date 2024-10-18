function formatearFecha(fecha) {

    // Extraer solo fecha, sin hora
    const dateString = fecha.split(" ")[2] + " " + fecha.split(" ")[1] + " " + fecha.split(" ")[3];

    const date = new Date(dateString); 
    const year = date.getFullYear();
    const month = ("0" + (date.getMonth() + 1)).slice(-2);  
    const day = ("0" + date.getDate()).slice(-2); 

    const formattedDate = `${year}-${month}-${day}`;
    
    return formattedDate;
}


function cargarDatosDocente(id, nombre, apellido, fechaNacimiento, correo, estado) {

    document.getElementById("docenteId").value = id;
    document.getElementById("editNombre").value = nombre;
    document.getElementById("editApellido").value = apellido;

    // Verificar si la fecha está disponible y mostrar el resultado
    if (fechaNacimiento) {
        const formattedDate = formatearFecha(fechaNacimiento);
        document.getElementById("editFechaNacimiento").value = formattedDate || ""; // Si no se puede formatear, mostrar vacío
    } else {
        document.getElementById("editFechaNacimiento").value = ""; // Para evitar valores incorrectos
    }

    document.getElementById("editCorreo").value = correo;
    document.getElementById("editEstado").value = estado;

    // Mostrar el modal de edición
    let modal = new bootstrap.Modal(document.getElementById('editDocenteModal'));
    modal.show();
}




document.getElementById("editDocenteForm").addEventListener("submit", function(e) {
    e.preventDefault();

    // Obtener los datos del formulario
    const docenteId = document.getElementById("docenteId").value;
    const docenteData = {
        Nombre: document.getElementById("editNombre").value,
        Apellido: document.getElementById("editApellido").value,
        Fecha_de_Nacimiento: document.getElementById("editFechaNacimiento").value,
        Correo: document.getElementById("editCorreo").value,
        Estado: document.getElementById("editEstado").value
    };

    // Enviar la solicitud PUT a la API para actualizar
    fetch(`/api/docentes/${docenteId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(docenteData) // Convertir el objeto a JSON
    })
    .then(response => response.json())
    .then(data => {
        if (data.exito) {
            alert("Docente actualizado con éxito");
            location.reload(); // Recargar la página para mostrar los cambios
        } else {
            alert("Error al actualizar el docente");
        }
    })
    .catch(error => {
        console.error("Error al actualizar el docente:", error);
    });
});
