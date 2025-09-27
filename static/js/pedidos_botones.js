let pedidoSeleccionado = null;

function seleccionarPedido(id, tablaId, botonEditarId, evento) {
    // Guardar el ID seleccionado
    pedidoSeleccionado = id;

    // Actualizar el enlace del botón de edición
    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_pedido/${id}`;
    }

    // Limpiar las filas previamente seleccionadas
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    // Resaltar la fila seleccionada
    const filaActual = evento.currentTarget;
    filaActual.classList.add("selected");
}

function eliminarPedido(tablaId, botonEliminarId) {
    if (!pedidoSeleccionado) {
        alert(`Por favor, selecciona un pedido en la tabla ${tablaId} antes de eliminar.`);
        return;
    }
    if (confirm("¿Estás seguro de que deseas eliminar este pedido?")) {
        fetch(`/${botonEliminarId}/${pedidoSeleccionado}`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Pedido eliminado correctamente.");
                    window.location.reload();
                } else {
                    alert("Error al eliminar el pedido.");
                }
            })
            .catch(err => console.error("Error:", err));
    }
}
