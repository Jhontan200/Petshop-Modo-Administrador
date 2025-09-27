function filtrarTabla(inputId, tablaId, paginar = true) {
    const input = document.getElementById(inputId);
    const filtro = input.value.toLowerCase();
    const filas = document.querySelectorAll(`#${tablaId} tbody tr`);

    filas.forEach(fila => {
        const textoFila = fila.textContent.toLowerCase();
        fila.style.display = textoFila.includes(filtro) ? "" : "none";
    });

    if (paginar) {
        paginarTabla(tablaId, `paginacion-${tablaId}`, 10);
    }
}

function paginarTabla(tablaId, paginacionId, filasPorPagina = 10) {
    const tabla = document.getElementById(tablaId);
    const paginacion = document.getElementById(paginacionId);
    const filas = Array.from(tabla.querySelectorAll("tbody tr")).filter(f => f.style.display !== "none");
    const totalPaginas = Math.ceil(filas.length / filasPorPagina);

    let paginaActual = 1;

    function mostrarPagina(pagina) {
        const inicio = (pagina - 1) * filasPorPagina;
        const fin = inicio + filasPorPagina;

        filas.forEach((fila, i) => {
            fila.style.display = (i >= inicio && i < fin) ? "" : "none";
        });

        paginacion.innerHTML = "";
        for (let i = 1; i <= totalPaginas; i++) {
            const btn = document.createElement("button");
            btn.textContent = i;
            btn.className = (i === pagina) ? "pagina-activa" : "";
            btn.onclick = () => mostrarPagina(i);
            paginacion.appendChild(btn);
        }
    }

    mostrarPagina(paginaActual);
}

function exportarTablaCSV(tablaId) {
    const tabla = document.getElementById(tablaId);
    const encabezados = Array.from(tabla.querySelectorAll("thead th")).map(th => th.textContent.trim());
    const filas = Array.from(tabla.querySelectorAll("tbody tr")); // todas las filas

    let csv = encabezados.join(",") + "\n";

    filas.forEach(fila => {
        const datos = Array.from(fila.querySelectorAll("td")).map(td => `"${td.textContent.trim()}"`);
        csv += datos.join(",") + "\n";
    });

    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = `${tablaId}.csv`;
    enlace.click();
}

function exportarTablaJSON(tablaId) {
    const tabla = document.getElementById(tablaId);
    const encabezados = Array.from(tabla.querySelectorAll("thead th")).map(th => th.textContent.trim());
    const filas = Array.from(tabla.querySelectorAll("tbody tr")); // todas las filas

    const datos = filas.map(fila => {
        const celdas = fila.querySelectorAll("td");
        const filaObj = {};
        celdas.forEach((td, i) => {
            filaObj[encabezados[i]] = td.textContent.trim();
        });
        return filaObj;
    });

    const blob = new Blob([JSON.stringify(datos, null, 2)], { type: "application/json" });
    const enlace = document.createElement("a");
    enlace.href = URL.createObjectURL(blob);
    enlace.download = `${tablaId}.json`;
    enlace.click();
}

document.addEventListener("DOMContentLoaded", () => {
    const tablas = [
        { idTabla: "tablaAdministradores", idPaginacion: "paginacion-tablaAdministradores" },
        { idTabla: "tablaClientes", idPaginacion: "paginacion-tablaClientes" },
        { idTabla: "tablaPedidos", idPaginacion: "paginacion-tablaPedidos" },
        { idTabla: "tablaProductos", idPaginacion: "paginacion-tablaProductos" },
        { idTabla: "tablaCategorias", idPaginacion: "paginacion-tablaCategorias" },
        { idTabla: "tablaVentas", idPaginacion: "paginacion-tablaVentas" },
        // Añade más si tienes otras tablas
    ];

    tablas.forEach(({ idTabla, idPaginacion }) => {
        const tabla = document.getElementById(idTabla);
        const paginacion = document.getElementById(idPaginacion);

        if (tabla && paginacion) {
            paginarTabla(idTabla, idPaginacion, 10);
        }
    });
});
