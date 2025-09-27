let contadorProductos = 0; // Contador global para asignar identificadores únicos

// Función para eliminar un producto específico del DOM
function eliminarProducto(idDetalle) {
    const detalle = document.getElementById(idDetalle);
    if (detalle) {
        detalle.remove();
    }
}

// Función para agregar nuevos productos dinámicamente usando <input list="listaProductos">
function agregarProductos() {
    const cantidadProductos = document.getElementById("cantidad_productos").value.trim();
    const productosContainer = document.getElementById("productosContainer");

    if (!cantidadProductos || isNaN(cantidadProductos) || cantidadProductos <= 0) {
        alert("Por favor, ingresa una cantidad válida de productos nuevos.");
        return;
    }

    for (let i = 1; i <= cantidadProductos; i++) {
        contadorProductos++;
        const nuevoDetalle = document.createElement("div");
        nuevoDetalle.className = "form-group producto-detalle";
        nuevoDetalle.id = `nuevo_detalle_${contadorProductos}`;
        nuevoDetalle.innerHTML = `
            <label for="id_producto_nuevo_${contadorProductos}">Producto:</label>
            <input list="listaProductos" id="id_producto_nuevo_${contadorProductos}" name="id_producto[]" placeholder="Buscar producto..." required>
            <label for="cantidad_nuevo_${contadorProductos}">Cantidad:</label>
            <input type="number" id="cantidad_nuevo_${contadorProductos}" name="cantidad[]" placeholder="Cantidad" required>
            <button type="button" class="boton-icono" onclick="eliminarProducto('nuevo_detalle_${contadorProductos}')">🗑️</button>
        `;
        productosContainer.appendChild(nuevoDetalle);
    }
}

// Función para validar y enviar el formulario de edición
async function verificarPedido() {
    const form = document.getElementById("formularioEditarPedido");
    const idCliente = document.getElementById("id_cliente").value.trim();
    const idAdministrador = document.getElementById("id_administrador").value.trim();
    const estado = document.getElementById("estado").value.trim();
    const fecha = document.getElementById("fecha").value.trim();
    const productosContainer = document.getElementById("productosContainer");
    const idProductos = productosContainer.querySelectorAll("input[name='id_producto[]']");
    const cantidades = productosContainer.querySelectorAll("input[name='cantidad[]']");

    let errores = [];

    // Validaciones locales
    if (!idCliente) errores.push("El cliente es obligatorio.");
    if (!idAdministrador) errores.push("El administrador es obligatorio.");
    if (!estado) errores.push("El estado es obligatorio.");
    if (!fecha) errores.push("La fecha es obligatoria.");
    if (idProductos.length === 0 || cantidades.length === 0) {
        errores.push("Debe agregar al menos un producto.");
    }

    idProductos.forEach((producto, index) => {
        const cantidad = cantidades[index]?.value.trim();
        if (!producto.value.trim()) errores.push(`El producto #${index + 1} es obligatorio.`);
        if (!cantidad || cantidad <= 0) errores.push(`La cantidad del producto #${index + 1} debe ser mayor a 0.`);
    });

    if (errores.length > 0) {
        alert(errores.join("\n"));
        return;
    }

    // Verificaciones en el servidor
    try {
        const clienteExiste = await fetch(`/verificar_cliente/${idCliente}`).then(res => res.json());
        if (!clienteExiste.existe) errores.push("El cliente no existe.");

        const administradorExiste = await fetch(`/verificar_administrador/${idAdministrador}`).then(res => res.json());
        if (!administradorExiste.existe) errores.push("El administrador no existe.");

        for (let i = 0; i < idProductos.length; i++) {
            const productoId = idProductos[i].value.trim();
            const productoExiste = await fetch(`/verificar_producto/${productoId}`).then(res => res.json());
            if (!productoExiste.existe) errores.push(`El producto #${i + 1} no existe.`);
        }

        if (errores.length > 0) {
            alert(errores.join("\n"));
            return;
        }

        form.submit();
    } catch (error) {
        console.error("Error al verificar datos:", error);
        alert("Hubo un problema al validar los datos. Intenta nuevamente.");
    }
}
