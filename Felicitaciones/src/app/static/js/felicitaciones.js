const apiUrl = '/api/felicitaciones';
let currentPage = 1;
const perPage = 4;

async function fetchFelicitaciones(page = 1) {
    try {
        // Fetch data from API with pagination
        const response = await fetch(`${apiUrl}?page=${page}&per_page=${perPage}`);
        const data = await response.json();

        // Check if the request was successful
        if (response.ok) {
            renderTable(data.felicitaciones);
            renderPagination(data.total_pages, data.page);
        } else {
            console.error('Error fetching felicitaciones:', data.message);
        }
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Function to render table rows
function renderTable(felicitaciones) {
    const itemsList = document.getElementById('items-list');
    itemsList.innerHTML = ''; // Clear existing rows

    // Iterate through felicitaciones data and create table rows
    felicitaciones.forEach(felicitacion => {
        const row = document.createElement('tr');

        const pdfLink = felicitacion.PDF ? `
        <a href="${felicitacion.PDF}" target="_blank" title="Ver PDF">
            <i class="fas fa-file-pdf fa-2x"></i>
        </a>
            ` : 'No PDF';
    
        row.innerHTML = `
            <td>${felicitacion.ID_felicitacion}</td>
            <td>${felicitacion.Docente}</td>  <!-- Display full name -->
            <td>${felicitacion.Fecha_de_ejecucion}</td>
            <td>${felicitacion.ID_sistema}</td>
            <td>${pdfLink}</td>
        `;
        itemsList.appendChild(row);
    });
}

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
            fetchFelicitaciones(i);
        });

        pageItem.appendChild(pageLink);
        pagination.appendChild(pageItem);
    }
}


document.getElementById("buscar-docentes-btn").addEventListener("click", function() {
    const nombre = document.getElementById("nombre").value;
    const fecha = document.getElementById("fecha").value;

    // Call the API to fetch docentes based on filters
    fetchFilteredFelicitaciones(nombre, fecha);
});

// Function to make API call with filters
function fetchFilteredFelicitaciones(nombre, fecha) {
    let url = '/api/felicitaciones?'; // Your API endpoint

    if (nombre) {
        url += `idDocente=${nombre}&`;
    }
    if (fecha) {
        url += `fecha=${fecha}&`;
    }

    // Make the API request with the filters
    fetch(url)
        .then(response => response.json())
        .then(data => {
            // Populate the table with the filtered data
            renderTable(data.felicitaciones); // Assuming renderTable function handles displaying the data
        })
        .catch(error => {
            console.error('Error fetching filtered data:', error);
        });
}

// Function to reset all filters
function reiniciarFiltros() {
    document.getElementById("nombre").value = '';
    document.getElementById("fecha").value = '';
    fetchFilteredFelicitaciones('', '');  // Fetch all data without filters
}




// Initial fetch for the first page of felicitaciones
fetchFelicitaciones();

if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}