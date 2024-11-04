function actualizarPaginacion(page, totalPages) {
    const paginationElement = document.querySelector('.pagination');
    paginationElement.innerHTML = '';

    // Boton ant
    if (page > 1) {
        const prev = document.createElement("li");
        prev.className = "page-item";
        prev.innerHTML = `<a class="page-link" href="#" onclick="cargarDocentes(${page - 1})">Anterior</a>`;
        paginationElement.appendChild(prev);
    }

    // Num de Pag
    for (let i = 1; i <= totalPages; i++) {
        const pageItem = document.createElement("li");
        pageItem.className = `page-item ${i === page ? 'active' : ''}`;
        pageItem.innerHTML = `<a class="page-link" href="#" onclick="cargarDocentes(${i})">${i}</a>`;
        paginationElement.appendChild(pageItem);
    }

    // Boton sig
    if (page < totalPages) {
        const next = document.createElement("li");
        next.className = "page-item";
        next.innerHTML = `<a class="page-link" href="#" onclick="cargarDocentes(${page + 1})">Siguiente</a>`;
        paginationElement.appendChild(next);
    }
}
