let categoriaSeleccionada = null; // Variable para almacenar el ID de la categoría seleccionada

// Función para seleccionar una categoría
function seleccionarCategoria(id, tablaId, botonEditarId, evento) {
    // Guardar el ID de la categoría seleccionada
    categoriaSeleccionada = id;

    // Actualizar el enlace del botón de edición
    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_categoria/${id}`;
    }

    // Limpiar las filas previamente seleccionadas
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    // Resaltar la fila seleccionada
    const filaActual = evento.currentTarget;
    filaActual.classList.add("selected");
}

// Función para eliminar una categoría
function eliminarCategoria(tablaId, botonEliminarId) {
    if (!categoriaSeleccionada) {
        alert(`Por favor, selecciona una categoría en la tabla ${tablaId} antes de eliminar.`);
        return;
    }
    if (confirm("¿Estás seguro de que deseas eliminar esta categoría?")) {
        fetch(`/${botonEliminarId}/${categoriaSeleccionada}`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Categoría eliminada correctamente.");
                    window.location.reload();
                } else {
                    alert("Error al eliminar la categoría.");
                }
            })
            .catch(err => console.error("Error al eliminar la categoría:", err));
    }
}
