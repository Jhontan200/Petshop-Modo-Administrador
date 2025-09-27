let ventaSeleccionada = null; // Variable para almacenar el ID de la venta seleccionada

// Función para seleccionar una venta
function seleccionarVenta(id, tablaId, botonEditarId, evento) {
    // Guardar el ID de la venta seleccionada
    ventaSeleccionada = id;

    // Actualizar el enlace del botón de edición
    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_venta/${id}`;
    }

    // Limpiar las filas previamente seleccionadas
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    // Resaltar la fila seleccionada
    const filaActual = evento.currentTarget;
    filaActual.classList.add("selected");
}

// Función para eliminar una venta
function eliminarVenta(tablaId, botonEliminarId) {
    if (!ventaSeleccionada) {
        alert(`Por favor, selecciona una venta en la tabla ${tablaId} antes de eliminar.`);
        return;
    }
    if (confirm("¿Estás seguro de que deseas eliminar esta venta?")) {
        fetch(`/${botonEliminarId}/${ventaSeleccionada}`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Venta eliminada correctamente.");
                    window.location.reload();
                } else {
                    alert("Error al eliminar la venta.");
                }
            })
            .catch(err => console.error("Error al eliminar la venta:", err));
    }
}
