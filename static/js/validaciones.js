document.getElementById("formularioAdministrador").addEventListener("submit", function (event) {
    let nombre = document.getElementById("nombre").value.trim();
    let apellidoPaterno = document.getElementById("apellido_paterno").value.trim();
    let usuario = document.getElementById("usuario").value.trim();
    let contrasena = document.getElementById("contrasena").value;
    let fechaIngreso = document.getElementById("fecha_ingreso").value; // Obtenemos el valor de tipo date

    let errores = [];

    // Validar campos obligatorios
    if (!nombre) errores.push("El nombre es obligatorio.");
    if (!apellidoPaterno) errores.push("El apellido paterno es obligatorio.");
    if (!usuario) errores.push("El usuario es obligatorio.");
    if (!contrasena || contrasena.length < 8) {
        errores.push("La contraseña debe tener al menos 8 caracteres.");
    }

    // Validar que se haya seleccionado una fecha válida
    if (!fechaIngreso) errores.push("La fecha de ingreso es obligatoria.");

    // Si hay errores, mostramos una alerta y evitamos el envío
    if (errores.length > 0) {
        event.preventDefault();
        alert(errores.join("\n"));
    }
});
function submitForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.submit(); // Enviar el formulario manualmente
    } else {
        console.error(`No se encontró el formulario con el id "${formId}".`);
    }
}
