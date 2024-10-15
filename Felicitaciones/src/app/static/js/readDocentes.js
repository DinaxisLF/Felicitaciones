document.addEventListener("DOMContentLoaded", function(){
    // Fetch data from the API
    fetch('/api/docentes')
    .then(response => response.json())
    .then(data => {
        
        //Data is an array containing one inner array
        const itemsList = document.getElementById('items-list');

        // Access the first element of data (which is the inner array)
        if (Array.isArray(data) && data.length > 0) {
            const outerList = data[0];  // Access the first inner list

            // Ensure that outerList is indeed an array before calling forEach
            if (Array.isArray(outerList)) {
                outerList.forEach(item => {
                    // Create a list item (li) element
                    const listItem = document.createElement('li');

                    // Add text content with item name and description
                    listItem.textContent = `${item.Nombre} - ${item.Apellido}`;

                    // Append the list item to the unordered list (ul)
                    itemsList.appendChild(listItem);
                });
            } else {
                console.error('outerList is not an array:', outerList);
            }
        } else {
            console.error('Data is not in the expected format:', data);
        }
    })
    .catch(error => console.error('Error fetching data:', error));

})

