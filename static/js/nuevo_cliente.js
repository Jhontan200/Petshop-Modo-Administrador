function guardarCliente() {
    // Referencia al formulario
    const form = document.getElementById("formularioAñadirCliente");

    // Obtener valores de los campos
    const nombre = document.getElementById("nombre").value.trim();
    const apellidoPaterno = document.getElementById("apellido_paterno").value.trim();
    const apellidoMaterno = document.getElementById("apellido_materno").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value.trim();

    let errores = []; // Lista para almacenar mensajes de error

    // Validaciones
    if (!nombre) errores.push("El nombre es obligatorio.");
    if (!apellidoPaterno) errores.push("El apellido paterno es obligatorio.");
    if (!usuario) errores.push("El usuario es obligatorio.");
    if (!contrasena || contrasena.length !== 8) {
        errores.push("La contraseña debe tener exactamente 8 caracteres.");
    }

    // Mostrar errores si los hay
    if (errores.length > 0) {
        alert(errores.join("\n"));
        return; // Detener el envío si hay errores
    }

    // Enviar el formulario si todo está bien
    form.submit();
}
