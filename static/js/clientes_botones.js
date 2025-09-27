let clienteSeleccionado = null;

function seleccionarCliente(id, tablaId, botonEditarId, evento) {
    // Guardar el ID seleccionado
    clienteSeleccionado = id;

    // Actualizar el enlace del botón de edición
    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_cliente/${id}`;
    }

    // Limpiar las filas previamente seleccionadas
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    // Resaltar la fila seleccionada
    const filaActual = evento.currentTarget;
    filaActual.classList.add("selected");
}

function eliminarCliente(tablaId, botonEliminarId) {
    if (!clienteSeleccionado) {
        alert(`Por favor, selecciona un cliente en la tabla ${tablaId} antes de eliminar.`);
        return;
    }
    if (confirm("¿Estás seguro de que deseas eliminar este cliente?")) {
        fetch(`/${botonEliminarId}/${clienteSeleccionado}`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Cliente eliminado correctamente.");
                    window.location.reload();
                } else {
                    alert("Error al eliminar el cliente.");
                }
            })
            .catch(err => console.error("Error:", err));
    }
}
