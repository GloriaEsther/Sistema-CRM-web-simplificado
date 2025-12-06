document.addEventListener('DOMContentLoaded', function() {
    hookupCrearForm();
    hookupEditarForm();
    hookupEliminarForm();
});

function getCsrf() {
    // Función estándar para obtener el token CSRF
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}

/* --------------- ABRIR MODALES Y TRAER DATOS --------------- */
function abrirConsultar(id) {
    // Usaremos la vista AJAX para obtener todos los detalles del cliente
    fetch('/clientes/ajax/consultar/' + id + '/') 
        .then(r => r.json())
        .then(data => {
            // Rellenar Modal Consultar Cliente
            document.getElementById('cons-nombre').textContent = data.nombre;
            document.getElementById('cons-apellido-paterno').textContent = data.apellidopaterno;
            document.getElementById('cons-apellido-materno').textContent = data.apellidomaterno;
            document.getElementById('cons-telefono').textContent = data.numerotelcli;
            document.getElementById('cons-correo').textContent = data.correo;
            document.getElementById('cons-direccion').textContent = data.direccion;
            document.getElementById('cons-rfc').textContent = data.rfc || 'N/A';
            document.getElementById('cons-fecha-nacimiento').textContent = data.fecha_nacimiento_display;
            document.getElementById('cons-estado').textContent = data.estado_cliente;
            document.getElementById('cons-frecuencia').textContent = data.frecuencia_compra;
            document.getElementById('cons-ultimo-contacto').textContent = data.fecha_ultimocontacto_display;
            document.getElementById('cons-comentarios').textContent = data.comentarios || 'Sin comentarios.';
            
            new bootstrap.Modal(document.getElementById('modalConsultarCliente')).show();
        })
        .catch(err => {
             console.error('Error al cargar datos del cliente para consultar:', err);
             // Puedes implementar un modal de error aquí en lugar de alert cuando tenga tiempo jajaj :')
        });
}

function abrirEditar(id) {
    // Usaremos la vista AJAX para obtener todos los detalles del cliente
    fetch('/clientes/ajax/consultar/' + id + '/')
        .then(r => r.json())
        .then(d => {
            // Rellenar Modal Editar Cliente
            document.getElementById('editar-id').value = id;
            document.getElementById('editar-nombre').value = d.nombre;
            document.getElementById('editar-apellidopaterno').value = d.apellidopaterno;
            document.getElementById('editar-apellidomaterno').value = d.apellidomaterno;
            document.getElementById('editar-numerotelcli').value = d.numerotelcli;
            document.getElementById('editar-correo').value = d.correo;
            document.getElementById('editar-direccion').value = d.direccion;
            document.getElementById('editar-rfc').value = d.rfc;
            document.getElementById('editar-fecha_nacimiento').value = d.fecha_nacimiento_iso;
            document.getElementById('editar-fecha_ultimocontacto').value = d.fecha_ultimocontacto_iso;
            document.getElementById('editar-comentarios').value = d.comentarios || '';

            // Seleccionar el valor correcto en los selects (Estado y Frecuencia)
            document.getElementById('editar-estado-cliente').value = d.estado_cliente_id;
            document.getElementById('editar-frecuencia-compra').value = d.frecuencia_compra_id;

            new bootstrap.Modal(document.getElementById('modalEditarCliente')).show();
        })
        .catch(err => {
             console.error('Error al cargar datos del cliente para editar:', err);
        });
}

function abrirEliminar(id, nombre) {
    // Para eliminar, solo necesitamos el ID y el nombre para la confirmación
    document.getElementById('eliminar-id').value = id;
    document.getElementById('elim-nombre').textContent = nombre; // Usamos el nombre que viene directo del template de la lista
    new bootstrap.Modal(document.getElementById('modalEliminarCliente')).show();
}

/* --------------- FORM CREAR (submit por redirección o fetch) --------------- */
function hookupCrearForm() {
    const form = document.getElementById('formCrearCliente');
    if (!form) return;
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        const data = new FormData(form);
        fetch('/clientes/crear/', { // Asegúrate de que esta URL es correcta
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            body: data
        }).then(r => {
            // Si el backend te devuelve una redirección (Solución Rápida), se recarga la página
            if (r.redirected) window.location = r.url; 
            else return r.text();
        }).then(txt => {
            if (txt && txt.includes('<form')) {
                // Esto podría ser un HTML con errores de Django
                alert('Errores en el formulario de creación. Revisa los campos.');
            }
        }).catch(e => console.error('Error al crear cliente:', e));
    });
}

/* --------------- FORM EDITAR --------------- */
function hookupEditarForm() {
    const form = document.getElementById('formEditarCliente');
    if (!form) return;
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        const id = document.getElementById('editar-id').value;
        const data = new FormData(form);

        fetch('/clientes/editar/' + id + '/', { // Asegúrate de que esta URL es correcta
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            body: data
        }).then(r => {
            if (r.redirected) window.location = r.url;
            else return r.text();
        }).then(txt => {
            if (txt && txt.includes('<form')) alert('Errores en la edición del cliente.');
        }).catch(e => console.error('Error al editar cliente:', e));
    });
}

/* --------------- FORM ELIMINAR --------------- */
function hookupEliminarForm() {
    const form = document.getElementById('formEliminarCliente');
    if (!form) return;
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        const id = document.getElementById('eliminar-id').value;
        const data = new FormData(form);
        
        fetch('/clientes/eliminar/' + id + '/', { // Asegúrate de que esta URL es correcta
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrf() },
            body: data
        }).then(r => {
            // Asumiendo que el backend siempre redirige a listar_clientes después de un éxito
            if (r.redirected) window.location = r.url;
            else console.error('No se pudo eliminar, el servidor no redirigió.');
        }).catch(e => console.error('Error al eliminar cliente:', e));
    });
}