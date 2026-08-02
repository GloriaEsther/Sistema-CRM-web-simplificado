document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("registroCobroForm");
  if (!form) return;

  const modalConfirmarEl = document.getElementById("confirmModal");
  const modalFaltantesEl = document.getElementById("faltantesModal");

  const modalConfirmar = modalConfirmarEl ? new bootstrap.Modal(modalConfirmarEl) : null;
  const modalFaltantes = modalFaltantesEl ? new bootstrap.Modal(modalFaltantesEl) : null;

  const btnConfirmar = document.getElementById("confirmarOpcionales");

  function hayCamposObligatoriosVacios() {
    const obligatorios = [
      { name: "forma_cobro", label: "Forma de cobro" },
      { name: "monto_recibido", label: "Monto" }
    ];

    const faltantes = obligatorios.filter(campo => {
      const el = form.querySelector(`[name="${campo.name}"]`);
      return !el || el.value.trim() === "";
    });

    if (faltantes.length > 0 && modalFaltantes) {
      const lista = document.getElementById("listaFaltantes");
      lista.innerHTML = "";
      faltantes.forEach(c => {
        const li = document.createElement("li");
        li.textContent = c.label;
        lista.appendChild(li);
      });
      modalFaltantes.show();
      return true;
    }
    return false;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (hayCamposObligatoriosVacios()) return;
    modalConfirmar?.show();
  });

  btnConfirmar?.addEventListener("click", function () {
    modalConfirmar.hide();
    form.submit();
  });
});
