document.addEventListener("DOMContentLoaded", function () {
    const logoutLink = document.getElementById("logout-link");

    // Mostrar siempre el botón de cerrar sesión
    logoutLink.style.display = "inline-flex";

    // Cerrar sesión
    logoutLink.addEventListener("click", function (e) {
        e.preventDefault();
        if (confirm("¿Seguro que quieres cerrar sesión?")) {
            // Redirigir al formulario de login
            location.href = "/login";

            // Eliminar posibilidad de volver con el botón "Atrás"
            history.replaceState(null, null, "/login");
        }
    });
});
