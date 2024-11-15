document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault(); 
            login(); 
        });
    } else {
        console.error("No se encontró el formulario de inicio de sesión");
    }
});

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch('/api/login', {  
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const messageDiv = document.getElementById("responseMessage");

        if (response.ok) {
            const result = await response.json();
            messageDiv.innerText = result.message;
            messageDiv.style.color = 'green';

            // Redirect on successful login
            window.location.href = "/docentes";  // Adjust this path as needed
        } else {
            const result = await response.json();
            messageDiv.innerText = result.message;
            messageDiv.style.color = 'red';
            console.log(result)
        }
    } catch (error) {
        console.error("Error en el login:", error);
        const messageDiv = document.getElementById("responseMessage");
        messageDiv.innerText = "Error en el servidor. Inténtelo más tarde.";
        messageDiv.style.color = 'red';
    }
}
