let graficoGenerado = false; // Variable para verificar si el gráfico ha sido generado

function mostrarOpcionesReporte() {
    const tipoReporte = document.getElementById("tipo_reporte").value;
    const opcionesFechas = document.getElementById("opciones-fechas");

    // Oculta el rango de fechas para Productos más vendidos
    if (tipoReporte === "productos_mas_vendidos") {
        opcionesFechas.style.display = "none"; // Oculta las fechas
    } else if (tipoReporte === "ventas") {
        opcionesFechas.style.display = "block"; // Muestra las fechas
    }
}

async function generarReporte() {
    const tipoReporte = document.getElementById("tipo_reporte").value;
    const fechaInicio = document.getElementById("fecha_inicio") ? document.getElementById("fecha_inicio").value : "";
    const fechaFin = document.getElementById("fecha_fin") ? document.getElementById("fecha_fin").value : "";

    let parametros = "";

    if (tipoReporte === "productos_mas_vendidos") {
        // Para productos más vendidos no se necesita rango de fechas
        parametros = `tipo=${tipoReporte}`;
    } else if (tipoReporte === "ventas") {
        if (!fechaInicio || !fechaFin) {
            alert("Por favor, seleccione un rango de fechas.");
            return;
        }
        parametros = `tipo=${tipoReporte}&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    }

    // Actualiza el gráfico dinámicamente
    const img = document.getElementById("grafico-reporte");
    img.src = `/ver_grafico?${parametros}`;
    img.alt = "Gráfico actualizado.";

    // Controla si el gráfico fue generado con éxito
    img.onload = function () {
        graficoGenerado = true; // Marca el gráfico como generado
    };
    img.onerror = function () {
        graficoGenerado = false; // Marca error si el gráfico no se pudo cargar
        alert("No se pudo generar el gráfico. Verifique los datos y vuelva a intentarlo.");
    };
}

async function guardarReporte() {
    const tipoReporte = document.getElementById("tipo_reporte").value;
    const fechaInicio = document.getElementById("fecha_inicio") ? document.getElementById("fecha_inicio").value : "";
    const fechaFin = document.getElementById("fecha_fin") ? document.getElementById("fecha_fin").value : "";
    const formato = document.getElementById("formato").value;

    // Verifica si el gráfico fue generado antes de guardar el reporte
    if (!graficoGenerado) {
        alert("Debe generar un gráfico antes de guardar el reporte.");
        return;
    }

    let parametros = `tipo=${tipoReporte}&formato=${formato}`;
    if (tipoReporte === "ventas") {
        parametros += `&fecha_inicio=${fechaInicio}&fecha_fin=${fechaFin}`;
    }

    try {
        const response = await fetch(`/reporte`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: parametros,
        });

        if (response.ok) {
            // Descarga automáticamente el reporte
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `reporte.${formato === 'pdf' ? 'pdf' : 'zip'}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        } else {
            const errorText = await response.text();
            alert("Error al guardar el reporte: " + errorText);
        }
    } catch (error) {
        console.error("Error al guardar el reporte:", error);
        alert("Hubo un problema al guardar el reporte. Intenta nuevamente.");
    }
}
