// Función para eliminar docente
function eliminarDocente(id) {
    if (confirm("¿Estás seguro de que quieres eliminar este docente?")) {
        fetch(`/api/docentes/${id}`, {
            method: 'DELETE', 
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.exito) {
                alert("Docente eliminado correctamente");
                location.reload(); // Recargar la página para reflejar los cambios
            } else {
                alert("No se pudo eliminar el docente");
            }
        })
        .catch(error => {
            console.error("Error al eliminar el docente:", error);
        });
    }
}
