let elementoSeleccionado = null;

function seleccionarElemento(id, tablaId, botonEditarId, evento) {
    // Guardar el ID seleccionado
    elementoSeleccionado = id;

    // Actualizar el enlace del botón de edición
    const btnEditar = document.getElementById(botonEditarId);
    if (btnEditar) {
        btnEditar.href = `/editar_administrador/${id}`;
    }

    // Limpiar las filas previamente seleccionadas
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);
    filas.forEach(fila => fila.classList.remove("selected"));

    // Resaltar la fila seleccionada
    const filaActual = evento.currentTarget;
    filaActual.classList.add("selected");
}



function eliminarElemento(tablaId, botonEliminarId) {
    if (!elementoSeleccionado) {
        alert(`Por favor, selecciona un elemento de la tabla ${tablaId} antes de eliminar.`);
        return;
    }
    if (confirm("¿Estás seguro de que deseas eliminar este elemento?")) {
        fetch(`/${botonEliminarId}/${elementoSeleccionado}`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Elemento eliminado correctamente.");
                    window.location.reload();
                } else {
                    alert("Error al eliminar el elemento.");
                }
            })
            .catch(err => console.error("Error:", err));
    }
}
