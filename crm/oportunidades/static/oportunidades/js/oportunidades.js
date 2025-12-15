// oportunidades.js
document.addEventListener('DOMContentLoaded', function() {
  setupDragAndDrop();
  hookupEditarForm();
  hookupEliminarForm();
});

function getCsrf() {
   let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

/* --------------- DRAG & DROPfunction --------------- */

function setupDragAndDrop() {

  const columns = document.querySelectorAll('.kanban-column');

  document.querySelectorAll('.kanban-card').forEach(card => {

    card.addEventListener('dragstart', ev => {
      ev.dataTransfer.setData('text/plain', card.dataset.id);
      card.classList.add('moving');
    });

    card.addEventListener('dragend', () => {
      card.classList.remove('moving');
    });

  });

  columns.forEach(column => {

    const wrapper = column.querySelector('.cards-wrapper');

    column.addEventListener('dragover', ev => {
      ev.preventDefault();
      ev.dataTransfer.dropEffect = 'move';
    });

    column.addEventListener('drop', ev => {
      ev.preventDefault();

      const id = ev.dataTransfer.getData('text/plain');
      if (!id) return;

      const card = document.querySelector(`.kanban-card[data-id="${id}"]`);
      if (!card || !wrapper) return;

      wrapper.appendChild(card);

      moverOportunidad(id, column.dataset.etapaId);
    });

  });
}

function moverOportunidad(idoportunidad, etapa_id) {
  fetch('/oportunidades/mover/' + idoportunidad + '/', {//fetch(window.location.origin + '/oportunidades/mover/' + idoportunidad + '/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCsrf(),
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({ 'etapa_id': etapa_id })
  }).then(r => r.json()).then(resp => {
    if (!resp.ok) alert('Error al mover: ' + (resp.error || 'desconocido'));
  }).catch(err => alert('Error de red al mover oportunidad.'));
}

/*eventos de bootstrap */
document.addEventListener('shown.bs.dropdown', function (e) {
    const card = e.target.closest('.kanban-card');
    if (card) {
        card.classList.add('menu-open');
    }
});

document.addEventListener('hidden.bs.dropdown', function (e) {
    const card = e.target.closest('.kanban-card');
    if (card) {
        card.classList.remove('menu-open');
    }
});


/* --------------- ABRIR MODALES Y TRAER DATOS --------------- */
function abrirConsultar(id) {
  fetch('/oportunidades/ajax/consultar/' + id + '/')
    .then(r => r.json())
    .then(data => {
      document.getElementById('cons-nombre').textContent = data.nombre;
      document.getElementById('cons-cliente').textContent = data.cliente;
      document.getElementById('cons-usuario').textContent = data.usuario;
      document.getElementById('cons-valor').textContent = data.valor;
      document.getElementById('cons-fecha').textContent = data.fecha;
      document.getElementById('cons-etapa').textContent = data.etapa;
      document.getElementById('cons-comentarios').textContent = data.comentarios || '';
      new bootstrap.Modal(document.getElementById('modalConsultar')).show();
    });
}

function abrirEditar(id) {
  fetch('/oportunidades/ajax/consultar/' + id + '/')
    .then(r => r.json())
    .then(d => {
      document.getElementById('editar-id').value = id;
      document.getElementById('editar-nombre').value = d.nombre;
      document.getElementById('editar-valor').value = d.valor;
      // d.fecha iso => YYYY-MM-DD
      document.getElementById('editar-fecha').value = d.fecha_iso || '';
      document.getElementById('editar-etapa').value = d.etapa_id;
      document.getElementById('editar-cliente-display').value = d.cliente;
      document.getElementById('editar-cliente-id').value = d.cliente_id;
      document.getElementById('editar-usuario-display').value = d.user_display;
      document.getElementById('editar-usuario-id').value = d.usuario_id;
      document.getElementById('editar-comentarios').value = d.comentarios || '';
      new bootstrap.Modal(document.getElementById('modalEditar')).show();
    });
}

function abrirEliminar(id) {
  fetch('/oportunidades/ajax/consultar/' + id + '/')
    .then(r => r.json())
    .then(d => {
      document.getElementById('eliminar-id').value = id;
      document.getElementById('elim-nombre').textContent = d.nombre;
      new bootstrap.Modal(document.getElementById('modalEliminar')).show();
    });
}

/* --------------- FORM EDITAR --------------- */
function hookupEditarForm() {
  const form = document.getElementById('formEditar');
  if (!form) return;
  form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    const id = document.getElementById('editar-id').value;
    const data = new FormData(form);
    fetch('/oportunidades/editar/' + id + '/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf() },
      body: data
    }).then(r => {
      if (r.redirected) window.location = r.url;
      else return r.text();
    }).then(txt => {
      if (txt && txt.includes('<form')) alert('Errores en la edición.');
    }).catch(e => alert('Error al editar oportunidad.'));
  });
}

/* --------------- FORM ELIMINAR --------------- */
function hookupEliminarForm() {
  const form = document.getElementById('formEliminar');
  if (!form) return;
  form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    const id = document.getElementById('eliminar-id').value;
    const data = new FormData(form);
    fetch('/oportunidades/eliminar/' + id + '/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrf() },
      body: data
    }).then(r => {
      if (r.redirected) window.location = r.url;
      else alert('No se pudo eliminar.');
    }).catch(e => alert('Error al eliminar.'));
  });
}

/* --------------- BÚSQUEDA AJAX: cliente y vendedor --------------- */
let currentSearchTarget = null; // '#modalCrear' o '#modalEditar'
// Obtener el prefijo ('crear' o 'editar')
function getPrefix() {
    if (!currentSearchTarget) return '';
    const base = currentSearchTarget.split('|')[0];
    return base.includes('Crear') || base.includes('crear') ? 'crear' : 'editar';
}

function abrirBuscarCliente(modalSelector) {
  currentSearchTarget = modalSelector;
  const prefix = getPrefix();
  // mostrar panel de busqueda dentro del modal (usa el panel con id -buscarPanel)
  document.getElementById(prefix +'-buscarPanel').style.display = 'block';
  document.getElementById(prefix +'-buscar-input').focus();
}

function abrirBuscarVendedor(modalSelector) {
  currentSearchTarget = modalSelector + '|vendedor';
  const prefix = getPrefix();
  document.getElementById(prefix + '-buscarPanel').style.display = 'block';
  document.getElementById(prefix + '-buscar-input').focus();
}

function busquedaAjax() {
  const prefix = getPrefix();
  const q = document.getElementById(prefix + '-buscar-input').value;
  const cont = document.getElementById(prefix + '-buscar-resultados');
  const url = currentSearchTarget && currentSearchTarget.includes('vendedor') ? '/oportunidades/ajax/buscar_vendedor/?q=' + encodeURIComponent(q) : '/oportunidades/ajax/buscar_cliente/?q=' + encodeURIComponent(q);
  
  fetch(url).then(r => r.json()).then(arr => {
    cont.innerHTML = '';
    arr.forEach(item => {
      const a = document.createElement('a');
      a.href = '#';
      a.className = 'list-group-item list-group-item-action';
      a.textContent = item.display;
      a.onclick = e => {
        e.preventDefault();
        // llenar el modal correcto (crear o editar)
        if (!currentSearchTarget) return;
        let isV = currentSearchTarget.includes('vendedor');
        // Asignación de valores al campo de visualización y al campo oculto de ID
        document.getElementById(prefix + (isV ? '-usuario-display' : '-cliente-display')).value = item.display;
        document.getElementById(prefix + (isV ? '-usuario-id' : '-cliente-id')).value = item.id;
                
        // Ocultar el panel de búsqueda correcto
        document.getElementById(prefix + '-buscarPanel').style.display = 'none';
        document.getElementById(prefix + '-buscar-input').value = '';
      };
      cont.appendChild(a);
    });
  });
}
