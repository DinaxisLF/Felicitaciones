document.getElementById("addDocenteForm").addEventListener("submit", function(e) {
    e.preventDefault(); 

    const nuevoDocente = {
        Nombre: document.getElementById("nombreAnadir").value,
        Apellido: document.getElementById("apellido").value,
        Fecha_de_Nacimiento: document.getElementById("fechaNacimiento").value,
        Correo: document.getElementById("correo").value,
        Estado: document.getElementById("estadoAnadir").value
    };

    fetch('/api/docentes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoDocente) 
    })
    .then(response => response.json())
    .then(data => {
        if (data.exito) {
            alert("Docente registrado con éxito");
            
            let modal = bootstrap.Modal.getInstance(document.getElementById('addDocenteModal'));
            modal.hide();
            
            location.reload();
        } else {
            alert("Error al registrar el docente");
        }
    })
    .catch(error => {
        console.error("Error al registrar el docente:", error);
    });
});
