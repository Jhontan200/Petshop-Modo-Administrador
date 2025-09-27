async function mostrarStockDisponible() {
    const idProducto = document.getElementById("id_producto").value.trim();
    const stockLabel = document.getElementById("stockDisponible");
    const campoCantidad = document.getElementById("cantidad");

    if (!idProducto || isNaN(idProducto)) {
        stockLabel.textContent = "";
        campoCantidad.disabled = false;
        campoCantidad.removeAttribute("max");
        campoCantidad.placeholder = "Cantidad vendida";
        return;
    }

    try {
        const res = await fetch(`/verificar_producto/${idProducto}`);
        const producto = await res.json();

        if (producto.existe) {
            if (producto.stock === 0) {
                stockLabel.textContent = `Producto '${producto.nombre}' sin stock disponible.`;
                stockLabel.style.color = "#FF0000";
                campoCantidad.disabled = true;
                campoCantidad.value = "";
                campoCantidad.placeholder = "Sin stock";
            } else {
                stockLabel.textContent = `Stock disponible de '${producto.nombre}': ${producto.stock} unidades`;
                stockLabel.style.color = "#6D5130";
                campoCantidad.disabled = false;
                campoCantidad.max = producto.stock;
                campoCantidad.placeholder = `Máximo: ${producto.stock}`;
            }
        } else {
            stockLabel.textContent = "Producto no encontrado.";
            stockLabel.style.color = "#FF0000";
            campoCantidad.disabled = false;
            campoCantidad.removeAttribute("max");
            campoCantidad.placeholder = "Cantidad vendida";
        }
    } catch (error) {
        console.error("Error al consultar el stock:", error);
        stockLabel.textContent = "Error al consultar el stock.";
        stockLabel.style.color = "#FF0000";
        campoCantidad.disabled = false;
        campoCantidad.removeAttribute("max");
        campoCantidad.placeholder = "Cantidad vendida";
    }
}

async function verificarEdicionVenta() {
    const form = document.getElementById("formularioEditarVenta");
    const idProducto = document.getElementById("id_producto").value.trim();
    const cantidad = document.getElementById("cantidad").value.trim();
    const fecha = document.getElementById("fecha").value.trim();
    const hora = document.getElementById("hora").value.trim();

    let errores = [];

    if (!idProducto || isNaN(idProducto) || parseInt(idProducto) <= 0) {
        errores.push("El ID del producto debe ser un número válido mayor a 0.");
    }

    if (!cantidad || isNaN(cantidad) || parseInt(cantidad) <= 0) {
        errores.push("La cantidad vendida debe ser un número mayor a 0.");
    }

    if (!fecha) errores.push("La fecha de la venta es obligatoria.");
    if (!hora) errores.push("La hora de la venta es obligatoria.");

    if (errores.length > 0) {
        alert(errores.join("\n"));
        return;
    }

    try {
        const respuesta = await fetch(`/verificar_producto/${idProducto}`);
        const producto = await respuesta.json();

        if (!producto.existe) {
            alert("El producto ingresado no existe.");
            return;
        }

        if (producto.stock === 0) {
            alert(`El producto '${producto.nombre}' está agotado.`);
            return;
        }

        if (parseInt(cantidad) > producto.stock) {
            alert(`Stock insuficiente. Solo hay ${producto.stock} unidades disponibles de '${producto.nombre}'.`);
            return;
        }

        form.submit();
    } catch (error) {
        console.error("Error al verificar el producto:", error);
        alert("Hubo un problema al verificar el producto. Intenta nuevamente.");
    }
}

// Mostrar stock al cargar el formulario
window.addEventListener("DOMContentLoaded", mostrarStockDisponible);
