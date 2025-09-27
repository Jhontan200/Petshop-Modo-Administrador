let productoSeleccionado = null; // ID del producto seleccionado

// Selecciona una fila de producto en la tabla
function seleccionarProducto(id, tablaId, botonEditarId, evento) {
    productoSeleccionado = id;

    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_producto/${id}`;
        btnEditar.classList.add("activo");
    }

    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    evento.currentTarget.classList.add("selected");
}

// Elimina el producto seleccionado
function eliminarProducto(tablaId, rutaEliminar) {
    if (!productoSeleccionado) {
        alert("Selecciona un producto antes de eliminar.");
        return;
    }

    if (!confirm("¿Estás seguro de que deseas eliminar este producto?")) {
        return;
    }

    fetch(`/${rutaEliminar}/${productoSeleccionado}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(async response => {
        const resultado = await response.json();

        if (response.ok) {
            alert(resultado.mensaje || "Producto eliminado correctamente.");
            window.location.reload();
        } else if (response.status === 409) {
            alert(resultado.error || "Este producto está vinculado a pedidos y no puede eliminarse.");
        } else if (response.status === 404) {
            alert("El producto no fue encontrado.");
        } else {
            alert("Error al eliminar el producto.");
        }
    })
    .catch(err => {
        console.error("Error al eliminar el producto:", err);
        alert("Error de conexión. Intenta nuevamente.");
    });
}
