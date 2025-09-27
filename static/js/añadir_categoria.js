async function verificarCategoria() {
    const form = document.getElementById("formularioAñadirCategoria");
    const nombreCategoria = document.getElementById("nombre_categoria").value.trim();

    let errores = []; // Lista para almacenar errores

    // Validaciones locales
    if (!nombreCategoria) errores.push("El nombre de la categoría es obligatorio.");

    // Mostrar errores locales si los hay
    if (errores.length > 0) {
        alert(errores.join("\n"));
        return;
    }

    // Verificar existencia en la base de datos (nombre único)
    try {
        const existeCategoria = await fetch(`/verificar_nombre_categoria/${nombreCategoria}`).then(res => res.json());
        if (existeCategoria.existe) {
            alert("El nombre de la categoría ya existe. Por favor elige otro nombre.");
            return;
        }

        // Si todo es válido, enviar el formulario
        form.submit();
    } catch (error) {
        console.error("Error al verificar la categoría:", error);
        alert("Hubo un problema al verificar el nombre de la categoría. Intenta nuevamente.");
    }
}
