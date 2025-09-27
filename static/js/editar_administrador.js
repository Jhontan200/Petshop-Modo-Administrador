// Función de validación y envío de formulario para Editar Administrador
function guardarCambios() {
    const form = document.getElementById("formularioEditarAdministrador"); // Identificador del formulario

    // Obtener valores de los campos
    const nombre = document.getElementById("nombre").value.trim();
    const apellidoPaterno = document.getElementById("apellido_paterno").value.trim();
    const apellidoMaterno = document.getElementById("apellido_materno").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const contrasena = document.getElementById("contrasena").value.trim();
    const fechaIngreso = document.getElementById("fecha_ingreso").value.trim();
    const horaIngreso = document.getElementById("hora_ingreso").value.trim();
    const horaSalida = document.getElementById("hora_salida").value.trim();

    let errores = []; // Lista para almacenar errores

    // Validaciones de campos obligatorios
    if (!nombre) errores.push("El nombre es obligatorio.");
    if (!apellidoPaterno) errores.push("El apellido paterno es obligatorio.");
    if (!usuario) errores.push("El usuario es obligatorio.");
    if (!contrasena || contrasena.length !== 8) {
        errores.push("La contraseña debe tener exactamente 8 caracteres.");
    }
    if (!fechaIngreso) errores.push("La fecha de ingreso es obligatoria.");
    if (!horaIngreso) errores.push("La hora de ingreso es obligatoria.");
    if (!horaSalida) errores.push("La hora de salida es obligatoria.");

    // Mostrar errores si los hay
    if (errores.length > 0) {
        alert(errores.join("\n")); // Muestra los errores en una alerta
        return; // Detiene el envío si hay errores
    }

    // Si todo está correcto, enviar el formulario
    form.submit();
}
