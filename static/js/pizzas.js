function eliminarSeleccionados() {
    var form = document.getElementById('formEliminar');
    var formData = new FormData(form);

    // Agrega el token CSRF al FormData
    formData.append('csrf_token', '{{ csrf_token() }}');

    // Envía la solicitud AJAX
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/eliminar_registros', true);
    xhr.onload = function () {
        // Maneja la respuesta si es necesario
        console.log(xhr.responseText);
    };
    xhr.send(formData);
}