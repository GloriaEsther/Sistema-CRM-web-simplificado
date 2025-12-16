document.addEventListener("DOMContentLoaded", function () {
  console.log("clientes.js cargado");
  const form = document.getElementById("registroClienteForm");
  //if (!form) return;

  /* ==========================
     ELEMENTOS
  ========================== */
  const estadoCliente = document.getElementById("id_estado_cliente");
  const frecuenciaContainer = document.getElementById("frecuenciaContainer");
  const frecuenciaSelect = document.getElementById("id_frecuencia_compra");

  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");
  const btnDescartar = document.getElementById("descartarOpcionales");

  const modalEliminarEl = document.getElementById("modalEliminarCliente");

  if (modalEliminarEl) {
    const modalEliminar = new bootstrap.Modal(modalEliminarEl);

    document.querySelectorAll(".btn-eliminar-cliente").forEach(btn => {
      btn.addEventListener("click", e => {
        e.preventDefault();
        console.log("CLICK ELIMINAR", btn.dataset.id, btn.dataset.nombre);
        const id = btn.dataset.id;
        const nombre = btn.dataset.nombre;

        document.getElementById("nombre").textContent = nombre;
        document.getElementById("btnConfirmarEliminar").href =
          `/clientes/${id}/eliminar/`;

        modalEliminar.show();
      });
    });
  }

  if(form){//si formulario de crear existe...
    /* ==========================
      MOSTRAR / OCULTAR FRECUENCIA
    ========================== */
    const FRECUENTE_ID = "3"; // ajusta si cambia en BD

    function toggleFrecuencia() {//function toggleFrecuencia() {
      if (!estadoCliente || !frecuenciaContainer) return;

      if (estadoCliente.value === FRECUENTE_ID) {//if (estadoCliente.value === FRECUENTE_ID) {
        frecuenciaContainer.style.display = "block";
      } else {
        frecuenciaContainer.style.display = "none";
        if (frecuenciaSelect) frecuenciaSelect.value = "";
      }
    }

    toggleFrecuencia();
    if (estadoCliente) {
      estadoCliente.addEventListener("change", toggleFrecuencia);
    }

    /* ==========================
      VALIDAR CAMPOS OBLIGATORIOS
    ========================== */
    function hayCamposObligatoriosVacios() {
      const obligatorios = [
        { id: "id_nombre", label: "Nombre" },
        //{ id: "id_apellidopaterno", label: "Apellido Paterno" },
        //{ id: "id_apellidomaterno", label: "Apellido Materno" },
        { id: "id_numerotelcli", label: "Número Telefónico" }
      ];

      const faltantes = obligatorios.filter(campo => {
        const el = document.getElementById(campo.id);
        return !el || el.value.trim() === "";
      });

      if (faltantes.length > 0 && modalFaltantes) {
        const lista = document.getElementById("listaFaltantes");
        if (lista) {
          lista.innerHTML = "";
          faltantes.forEach(c => {
            const li = document.createElement("li");
            li.textContent = c.label;
            lista.appendChild(li);
          });
        }
        modalFaltantes.show();
        return true;
      }
      return false;
    }

    /* ==========================
      CONFIRMAR ANTES DE GUARDAR
    ========================== */
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      if (hayCamposObligatoriosVacios()) return;

      const tieneDatos = Array.from(form.elements).some(el =>
        el.value && el.value.trim() !== ""
      );

      if (tieneDatos && modalConfirmar) {
        modalConfirmar.show();
      } else {
        form.submit();
      }
    });

    /* ==========================
      BOTONES DEL MODAL
    ========================== */
    if (btnConfirmar) {
      btnConfirmar.addEventListener("click", function () {
        modalConfirmar.hide();
        form.submit();
      });
    }

    if (btnDescartar) {
      btnDescartar.addEventListener("click", function () {
        form.reset();
        toggleFrecuencia();
        modalConfirmar.hide();
      });
    }
  }
});