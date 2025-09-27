async function verificarProducto() {
    const form = document.getElementById("formularioAñadirProducto");
    const nombre = document.getElementById("nombre").value.trim();
    let precio = document.getElementById("precio").value.trim();
    const stock = document.getElementById("stock").value.trim();
    const idCategoria = document.getElementById("id_categoria").value.trim();
    const descripcion = document.getElementById("descripcion").value.trim();

    let errores = [];

    // Validaciones locales
    if (!nombre) errores.push("El nombre del producto es obligatorio.");

    if (!precio || isNaN(precio) || parseFloat(precio) <= 0) {
        errores.push("El precio debe ser un número válido mayor a 0. Usa punto para decimales.");
    } else {
        precio = precio.replace(",", ".");
        document.getElementById("precio").value = precio;
    }

    if (!stock || isNaN(stock) || parseInt(stock) <= 0) {
        errores.push("El stock debe ser un número entero mayor a 0.");
    }

    if (!idCategoria || isNaN(idCategoria)) {
        errores.push("La categoría debe ser un ID numérico válido.");
    }

    if (errores.length > 0) {
        alert(errores.join("\n"));
        return;
    }

    // Validación remota: verificar si la categoría existe
    try {
        const respuesta = await fetch(`/verificar_categoria/${idCategoria}`);
        const resultado = await respuesta.json();

        if (!resultado.existe) {
            alert("La categoría ingresada no existe. Por favor selecciona una válida.");
            return;
        }

        form.submit();
    } catch (error) {
        console.error("Error al verificar la categoría:", error);
        alert("Hubo un problema al verificar la categoría. Intenta nuevamente.");
    }
}
