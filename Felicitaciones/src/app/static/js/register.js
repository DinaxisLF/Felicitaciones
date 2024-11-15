document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("register-form");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Collect form data
        const nameInput = form.querySelector("input[placeholder='Nombre']");
        const emailInput = form.querySelector("input[type='email']");
        const passwordInput = form.querySelector("input[type='password']");
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Clear any previous messages
        let messageDiv = document.getElementById("message");
        if (messageDiv) messageDiv.remove();

        // Frontend validation
        if (!name || !email || !password) {
            messageDiv = document.createElement("div");
            messageDiv.id = "message";
            messageDiv.className = "alert alert-danger";
            messageDiv.innerText = "Todos los campos son necesarios.";
            form.insertAdjacentElement("beforebegin", messageDiv);
            return;
        }

        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, email, password }),
            });

            const result = await response.json();

            // Create message div
            messageDiv = document.createElement("div");
            messageDiv.id = "message";
            messageDiv.className = "alert";

            if (result.success) {
                messageDiv.classList.add("alert-success");
                messageDiv.innerText = "Admin registrado";
            } else {
                messageDiv.classList.add("alert-danger");
                messageDiv.innerText = "Error: " + result.message;
            }

            form.insertAdjacentElement("beforebegin", messageDiv);
        } catch (error) {
            // Show error message in case of network or other issues
            messageDiv = document.createElement("div");
            messageDiv.id = "message";
            messageDiv.className = "alert alert-danger";
            messageDiv.innerText = "An error occurred. Please try again.";

            form.insertAdjacentElement("beforebegin", messageDiv);
            console.error("Error:", error);
        }
    });
});


if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}