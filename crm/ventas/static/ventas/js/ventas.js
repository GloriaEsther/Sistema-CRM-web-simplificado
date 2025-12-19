document.addEventListener("DOMContentLoaded", function () {
  console.log("ventas.js cargado");

  const form = document.getElementById("registroVentaForm");

  /* ==========================
     MODALES
  ========================== */
  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");
  const btnDescartar = document.getElementById("descartarOpcionales");

  if (!form) return;

  /* ==========================
     VALIDAR CAMPOS OBLIGATORIOS
  ========================== */
  function hayCamposObligatoriosVacios() {
    const obligatorios = [
      { id: "id_nombreventa", label: "Nombre de la venta" },
      { id: "id_preciototal", label: "Precio total" },
      { id: "id_estatus_cobro", label: "Estatus de cobro" },
      { id: "id_oportunidad_venta", label: "Oportunidad" },
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

    modalConfirmar ? modalConfirmar.show() : form.submit();
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
      modalConfirmar.hide();
    });
  }
});
